import redis
from django.conf import settings
from store.models import Product


class Recommendations:
    r = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )

    def get_product_key(self, id):
        return 'product:{}:purchased_with'.format(id)

    def products_bought(self, products):
        product_ids = [p.id for p in products]

        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    self.r.zincrby(self.get_product_key(product_id), 1,
                                   with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only 1 product
            suggestions = self.r.zrange(
                self.get_product_key(product_ids[0]),
                0, -1, desc=True)[:max_results]
        else:
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            keys = [self.get_product_key(id) for id in product_ids]
            self.r.zunionstore(tmp_key, keys)
            self.r.zrem(tmp_key, *product_ids)
            suggestions = self.r.zrange(tmp_key, 0, -1,
                                        desc=True)[:max_results]
            self.r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(
            Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            self.r.delete(self.get_product_key(id))
