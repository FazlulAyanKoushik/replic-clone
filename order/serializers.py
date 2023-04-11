"""
    Serializer for Order
"""
from rest_framework import serializers

from cart.models import Cart
from order.models import Order
from product.serializers import ProductItemSerializer
from shipping_address.serializers import ShippingAddressOrderSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    item = ProductItemSerializer(read_only=True)
    # total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ["item", "quantity"]

    def get_total_price(self, obj):
        return obj.get_total_price()


class OrderSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressOrderSerializer(read_only=True)
    order_items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = "__all__"
