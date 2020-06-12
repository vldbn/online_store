from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()

router.register('ratings',views.RatingViewSet, basename='ratings')
urlpatterns = [
    path('users/', views.UsersAmount.as_view()),
    path('products/', views.ProductsAmount.as_view()),
    path('', include(router.urls))
]