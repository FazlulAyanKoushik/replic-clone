"""
    Views for Order
"""
import json

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.models import Cart
from order.models import Order
from shipping_address.models import ShippingAddress
from order.serializers import OrderSerializer

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# Create your views here
@permission_classes([IsAuthenticated])
class OrderList(APIView):
    """List or create new order"""

    def get(self, request, format=None):
        """get all orders of requested user"""
        try:
            orders = (
                Order.objects.select_related("shipping_address")
                .prefetch_related("order_items")
                .filter(user=request.user)
                .order_by("-created_at")
            )
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"msg": "User have no order"}, status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            return Response(
                {"msg": "please add shipping address"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            carts = Cart.objects.filter(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"msg": "No cart items selected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_price = 0
        delivery_charge = 100

        if shipping_address.city and shipping_address.city.lower() == "dhaka":
            delivery_charge = 50

        for cart in carts:
            total_price += cart.get_total_price()

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            delivery_charge=delivery_charge,
            total_price=delivery_charge + total_price,
        )
        order.order_items.set(carts)
        order.save()

        serializer = OrderSerializer(order)
        print("order data : ", serializer.data)
        return Response({"order": serializer.data}, status=status.HTTP_200_OK)
