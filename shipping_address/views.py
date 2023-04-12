"""
    Views for Shipping Address
"""
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shipping_address.models import ShippingAddress
from .serializers import ShippingAddressSerializer


# Create your views here.


@permission_classes([IsAuthenticated])
class CreateShippingAddress(APIView):
    """
    create a new Shipping Address.
    """

    serializer_class = ShippingAddressSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class ShippingAddressDetail(APIView):
    """
    Retrieve, update or delete a Shipping Address.
    """

    serializer_class = ShippingAddressSerializer

    def get(self, request, format=None):
        shipping_address = ShippingAddress.objects.get(user=request.user)
        serializer = self.serializer_class(shipping_address)
        return Response(serializer.data)

    def put(self, request, format=None):
        shipping_address = ShippingAddress.objects.get(user=request.user)
        serializer = self.serializer_class(shipping_address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        shipping_address = ShippingAddress.objects.get(user=request.user)
        shipping_address.delete()
        return Response(
            {"msg": "Shipping address deleted."}, status=status.HTTP_204_NO_CONTENT
        )
