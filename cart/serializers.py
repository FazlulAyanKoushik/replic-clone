"""
    Serializer for cart
"""
from rest_framework import serializers
from cart.models import Cart
from product.serializers import ProductItemSerializer


class CartSerializer(serializers.ModelSerializer):
    item = ProductItemSerializer(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, obj):
        return obj.get_total_price()
