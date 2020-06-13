from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from store.models import Product, Rating
from api.serializers import RatingSerializer, ProductSerializer


class RatingViewSet(ModelViewSet):
    """Returns Ratings."""

    serializer_class = RatingSerializer
    queryset = Rating.objects.all()


class ProductsViewSet(ModelViewSet):
    """Returns Products id's."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
