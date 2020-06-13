import falcon
from app import routes

app = falcon.API()

fit_model = routes.FitModel()
signin = routes.SignIn()
recommendations = routes.Recommendations()

app.add_route('/fit', fit_model)
app.add_route('/signin', signin)
app.add_route('/recommendations', recommendations)
