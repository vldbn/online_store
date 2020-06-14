import falcon
import json
import requests
import torch
import pandas as pd
from app.settings import RATINGS_URL, PRODUCTS_URL
from model import net

rating_url = RATINGS_URL
products_url = PRODUCTS_URL
recommendations_dict = {}


class FitModel(object):
    """Fit model after request."""

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        try:
            res = requests.get(rating_url)
            j = res.json()
        except requests.ConnectionError:
            print('Can not get data.')

        try:
            df = pd.DataFrame(j)
        except ValueError:
            print('Pandas can not read json')
            df = None

        if df is not None:
            df['new_user_id'] = df.apply(net.map_user_id, axis=1)
            df['new_product_id'] = df.apply(net.map_movie_id, axis=1)

            user_ids = df['new_user_id'].values
            product_ids = df['new_product_id'].values
            rate = df['rate'].values - 2.5

            Ntrain = int(0.6 * len(rate))
            train_users = user_ids[:Ntrain]
            train_products = product_ids[:Ntrain]
            train_ratings = rate[:Ntrain]

            test_users = user_ids[Ntrain:]
            test_products = product_ids[Ntrain:]
            test_ratings = rate[Ntrain:]

            net.fit(net.model, net.criterion, net.optimizer,
                    (train_users, train_products, train_ratings),
                    (test_users, test_products, test_ratings), epochs=5, bs=5)
            torch.save(net.model.state_dict(), './model/state')


class SignIn(object):
    """Returns ratings of all products for a user, save result in a
    dict with key - 'user_id' and value - {'product_id' : ratings}.
    For input: json {'user_id':1}."""

    def on_post(self, req, resp):

        try:
            raw_data = json.load(req.bounded_stream)
            user_id = raw_data.get('user_id')
        except json.JSONDecodeError:
            user_id = None

        if user_id:
            res_products = requests.get(products_url)
            j = res_products.json()

            df = pd.DataFrame(j)
            df = df.astype('int64')
            user_ids = [id for i in range(0, len(df['id']))]
            df.rename(columns={'id': 'product'}, inplace=True)
            df['user'] = user_ids
            df['new_user_id'] = df.apply(net.map_user_id, axis=1)
            df['new_product_id'] = df.apply(net.map_movie_id, axis=1)

            net.model.load_state_dict(torch.load('./model/state'))

            r_user = torch.from_numpy(df['new_user_id'].values)
            r_products = torch.from_numpy(df['new_product_id'].values)

            net.model.eval()
            result = net.model.forward(r_user, r_products)
            result = torch.sigmoid(result)
            df['result'] = result.data.numpy()

            result_dict = df.set_index('product')['result'].to_dict()
            usr_result_dict = {user_id: result_dict}
            recommendations_dict.update(usr_result_dict)
        resp.status = falcon.HTTP_200


class Recommendations(object):
    """For input gets user_id, get values from recommendations_dict by
    user_id, sort them from highest value and returns 6 product_id's."""

    def on_post(self, req, resp):
        try:
            raw_data = json.load(req.bounded_stream)
            user_id = raw_data.get('user_id')
        except json.JSONDecodeError:
            user_id = None

        if user_id:
            try:
                user_rec = recommendations_dict[user_id]
                user_rec_list_sorted = sorted(user_rec,
                                              key=user_rec.get, reverse=True)
                recommendations_list = user_rec_list_sorted[0:6]
                d = {'recommendations': recommendations_list}
                j = json.dumps(d)
                resp.status = falcon.HTTP_200
                resp.media = j
            except KeyError:
                print('No user_id in dict.')
                resp.status = falcon.HTTP_500
