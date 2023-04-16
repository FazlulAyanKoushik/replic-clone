"""
    views for Category and Discount
"""
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from category.models import Category, Discount
from category.serializers import CategorySerializer, DiscountSerializer
from product.models import Product
from product.serializers import ProductSerializer

import logging

logger = logging.getLogger(__name__)


# Create your views here.
class CategoryList(APIView):
    """List all categories or create a new category."""

    serializer_class = CategorySerializer

    def get(self, request):
        # Get all categories from the database
        categories = Category.objects.filter()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data)


class CategoryProductsBySlug(APIView):
    """Get by category products"""

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        category = self.get_object(slug)
        products = category.products.filter()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetail(APIView):
    """Retrieve a category instance."""

    serializer_class = CategorySerializer

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            logger.warning("Category not Found")
            raise Http404

    def get(self, request, slug):
        category = self.get_object(slug)
        serializer = self.serializer_class(category)
        return Response(serializer.data)


# @permission_classes([IsAdminUser])
# class CategoryUpdateDelete(APIView):
#     """Retrieve, update or delete a category instance."""
#
#     serializer_class = CategorySerializer
#
#     def get_object(self, slug):
#         try:
#             return Category.objects.get(slug=slug)
#         except Category.DoesNotExist:
#             raise Http404
#
#     @swagger_auto_schema(
#         request_body=serializer_class,
#     )
#     def put(self, request, slug):
#         # update a category by admin user
#         category = self.get_object(slug)
#         serializer = self.serializer_class(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, slug):
#         # delete a category by admin user
#         category = self.get_object(slug)
#         category.delete()
#         return Response(
#             {"msg": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT
#         )


"""Discount Views"""
#
#
# @permission_classes([IsAdminUser])
# class DiscountList(APIView):
#     """
#     List all snippets, or create a new Discount.
#     """
#
#     serializer_class = DiscountSerializer
#
#     def get(self, request, format=None):
#         discounts = Discount.objects.all()
#         serializer = self.serializer_class(discounts, many=True)
#         return Response(serializer.data)
#
#     @swagger_auto_schema(
#         request_body=serializer_class,
#     )
#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @permission_classes([IsAdminUser])
# class DiscountDetail(APIView):
#     """
#     Retrieve, update or delete a discount instance.
#     """
#
#     serializer_class = DiscountSerializer
#
#     def get_object(self, slug):
#         try:
#             return Discount.objects.get(slug=slug)
#         except Discount.DoesNotExist:
#             raise Http404
#
#     def get(self, request, slug, format=None):
#         discount = self.get_object(slug)
#         serializer = self.serializer_class(discount)
#         return Response(serializer.data)
#
#     @swagger_auto_schema(
#         request_body=serializer_class,
#     )
#     def put(self, request, slug, format=None):
#         discount = self.get_object(slug)
#         serializer = self.serializer_class(discount, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, slug, format=None):
#         discount = self.get_object(slug)
#         products = Product.objects.filter(category=discount.category)
#         for product in products:
#             product.discount_price = None
#             product.save()
#         discount.delete()
#         return Response(
#             {"msg": "Discount deleted successfully"}, status=status.HTTP_204_NO_CONTENT
#         )
