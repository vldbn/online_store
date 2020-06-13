from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()

router.register('ratings',views.RatingViewSet, basename='ratings')
router.register('products', views.ProductsViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls))
]