from rest_framework import serializers
from store.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """Rating model serializer"""

    class Meta:
        model = Rating
        fields = ['id', 'user', 'product', 'rate']
