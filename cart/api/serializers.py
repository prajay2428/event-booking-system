# cart/api/serializers.py

from rest_framework import serializers
from movies.models import Seat


class CartSeatSerializer(serializers.ModelSerializer):
    theatre = serializers.StringRelatedField()

    class Meta:
        model = Seat
        fields = [
            "id",
            "theatre",
            "name",
            "price",
            "category",
        ]


class CartItemSerializer(serializers.Serializer):
    seat = CartSeatSerializer()

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )