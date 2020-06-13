from rest_framework import serializers
from store.models import Rating, Product


class RatingSerializer(serializers.ModelSerializer):
    """Rating model serializer."""

    class Meta:
        model = Rating
        fields = ['id', 'user', 'product', 'rate']


class ProductSerializer(serializers.ModelSerializer):
    """Product model serializer."""

    class Meta:
        model = Product
        fields = ['id']
