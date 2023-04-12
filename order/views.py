"""
    Views for Order
"""

from datetime import datetime

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from order.models import Order
from order.serializers import OrderSerializer
from shipping_address.models import ShippingAddress


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
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class OrderDetail(APIView):
    """
    Retrieve a order instance.
    """

    serializer_class = OrderSerializer

    def get_object(self, uuid):
        try:
            return Order.objects.get(uuid=uuid)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        order = self.get_object(uuid)
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""
    Order Views for Admin User
"""


@permission_classes([IsAdminUser])
class AdminOrderList(APIView):
    """Get all orders for admin user"""

    serializer_class = OrderSerializer

    def get(self, request, format=None):
        """get all orders for admin user"""
        orders = (
            Order.objects.select_related("shipping_address")
            .prefetch_related("order_items")
            .filter()
        )
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class AdminOrderDetail(APIView):
    """Get any order detail for admin user by uuid"""

    serializer_class = OrderSerializer

    def get_object(self, uuid):
        """Helper method to get a single object"""
        try:
            return Order.objects.get(uuid=uuid)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        order = self.get_object(uuid)
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    def delete(self, request, uuid, format=None):
        order = self.get_object(uuid)
        order.delete()
        return Response(
            {"msg": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


@permission_classes([IsAdminUser])
class UpdateOrderToPaid(APIView):
    """Update order payment status"""

    serializer_class = OrderSerializer

    def get_object(self, uuid):
        """Helper method to get a single object"""
        try:
            return Order.objects.get(uuid=uuid)
        except Order.DoesNotExist:
            raise Http404

    def put(self, request, uuid, format=None):
        """update order payment status"""
        order = self.get_object(uuid)
        order.is_paid = True
        order.paid_at = datetime.now()
        order.save()
        return Response({"message": "Order paid"}, status=status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class UpdateOrderToDelivered(APIView):
    """Update order deliver status"""

    serializer_class = OrderSerializer

    def get_object(self, uuid):
        """Helper method to get a single object"""
        try:
            return Order.objects.get(uuid=uuid)
        except Order.DoesNotExist:
            raise Http404

    def put(self, request, uuid, format=None):
        """update order deliver status"""
        order = self.get_object(uuid)
        order.is_delivered = True
        order.delivered_At = datetime.now()
        order.save()
        return Response({"message": "Order delivered"}, status=status.HTTP_200_OK)
