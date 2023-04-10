"""
    Views for cart
"""
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

from cart.models import Cart
from cart.serializers import CartSerializer
from product.models import Product

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


@permission_classes([IsAuthenticated])
class CartList(APIView):
    serializer_class = CartSerializer

    def get_cart_object(self, user, product):
        try:
            return Cart.objects.get(user=user, item=product)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        """Get a cart list for authenticated user"""
        try:
            carts = Cart.objects.select_related('item').filter(user=request.user)
            serializer = self.serializer_class(carts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        """Carts calculation Here, increment or decreament product item quantity"""
        product_slug = request.data.get('product_slug')
        quantity = int(request.data.get('quantity', 1))
        action = request.data.get('action')
        product = get_object_or_404(Product.objects.filter(), slug=product_slug)

        if action == 'inc':
            """
                If action is inc then cart item quantity will increase 
                        and update and calculate all stuff.
            """

            if product.stock < quantity:
                return Response({
                    'error': 'Not enough stock.'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                """If the product already exists in cart item"""
                cart = Cart.objects.get(user=request.user, item=product)
                cart.quantity += quantity
                cart.save()
            except Cart.DoesNotExist:
                """If adding a new product in cart item"""
                cart = Cart.objects.create(
                    user=request.user,
                    item=product,
                    quantity=quantity
                )
                product.stock -= quantity
                product.save()

                serializer = self.serializer_class(cart)
                return Response(serializer.data, status=status.HTTP_200_OK)

        if action == 'dec':
            """
                If action is dec then cart item quantity will decrease
                            and update and calculate all stuff.
            """
            cart = self.get_cart_object(request.user, product)

            if cart.quantity <= quantity:
                cart.delete()
                product.stock += quantity
                product.save()
                return Response({
                    'msg': 'Cart item removed'
                }, status=status.HTTP_204_NO_CONTENT)
            else:
                cart.quantity -= quantity
                cart.save()

                product.stock += quantity
                product.save()

            serializer = self.serializer_class(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
