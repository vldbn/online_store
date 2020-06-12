from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from store.models import Product, Rating
from api.serializers import RatingSerializer


class UsersAmount(APIView):
    """Returns users amount."""

    def get(self, request):
        users = User.objects.all()
        response = {
            'total_users': users.count()
        }
        return Response(response)


class ProductsAmount(APIView):
    """Returns products amount."""

    def get(self, request):
        products = Product.objects.all()
        response = {
            'total_products': products.count()
        }
        return Response(response)


class RatingViewSet(ModelViewSet):
    """Returns Ratings."""

    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
