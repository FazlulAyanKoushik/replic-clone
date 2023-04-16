"""
    views for Admin Users
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
from product.models import Product, Tag
from product.serializers import (
    TagSerializer,
    ProductsSerializer,
)

# Create your views here.
"""Views For Category Admin"""


@permission_classes([IsAdminUser])
class CategoryCreate(APIView):
    """Create a category by Admin."""

    serializer_class = CategorySerializer

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def post(self, request):
        # create a category by admin user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAdminUser])
class CategoryUpdateDelete(APIView):
    """Retrieve, update or delete a category instance."""

    serializer_class = CategorySerializer

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def put(self, request, slug):
        # update a category by admin user
        category = self.get_object(slug)
        serializer = self.serializer_class(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        # delete a category by admin user
        category = self.get_object(slug)
        category.delete()
        return Response(
            {"msg": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


"""Views for Discount Admin"""


@permission_classes([IsAdminUser])
class DiscountList(APIView):
    """
    List all snippets, or create a new Discount.
    """

    serializer_class = DiscountSerializer

    def get(self, request, format=None):
        discounts = Discount.objects.all()
        serializer = self.serializer_class(discounts, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAdminUser])
class DiscountDetail(APIView):
    """
    Retrieve, update or delete a discount instance.
    """

    serializer_class = DiscountSerializer

    def get_object(self, slug):
        try:
            return Discount.objects.get(slug=slug)
        except Discount.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        discount = self.get_object(slug)
        serializer = self.serializer_class(discount)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def put(self, request, slug, format=None):
        discount = self.get_object(slug)
        serializer = self.serializer_class(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        discount = self.get_object(slug)
        products = Product.objects.filter(category=discount.category)
        for product in products:
            product.discount_price = None
            product.save()
        discount.delete()
        return Response(
            {"msg": "Discount deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


"""Views for Tag Admin"""


@permission_classes([IsAdminUser])
class TagList(APIView):
    """List all tags, or create a new tag."""

    serializer_class = TagSerializer

    def get(self, request, format=None):
        tags = Tag.objects.filter()
        serializer = self.serializer_class(tags, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAdminUser])
class TagDetail(APIView):
    """Retrieve, update or delete a tag instance."""

    serializer_class = TagSerializer

    def get_object(self, slug):
        try:
            return Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        tag = self.get_object(slug)
        serializer = self.serializer_class(tag)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def put(self, request, slug, format=None):
        tag = self.get_object(slug)
        serializer = self.serializer_class(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        tag = self.get_object(slug)
        tag.delete()
        return Response(
            {"msg": "Tag Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


"""Views for Product Admin"""


@permission_classes([IsAdminUser])
class ProductCreate(APIView):
    """Create product by admin user"""

    serializer_class = ProductsSerializer

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAdminUser])
class ProductUpdateDelete(APIView):
    """Product update and delete by admin"""

    serializer_class = ProductsSerializer

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def put(self, request, slug, format=None):
        product = self.get_object(slug)
        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def patch(self, request, slug, format=None):
        product = self.get_object(slug)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        product = self.get_object(slug)
        product.delete()
        return Response(
            {"msg": "Product Deleted successfully"}, status.HTTP_204_NO_CONTENT
        )
