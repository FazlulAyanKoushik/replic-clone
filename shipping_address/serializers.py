"""
    Serializer for Shipping Address
"""
from rest_framework import serializers
from shipping_address.models import ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)

    class Meta:
        model = ShippingAddress
        exclude = ["user"]


class ShippingAddressOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ["address", "city", "zipcode", "country"]
