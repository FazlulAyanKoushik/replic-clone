"""
    Views for Product, Tag and TagConnector connector models
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, Tag, TagConnector
from product.serializers import (
    ProductSerializer,
    SecondaryProductSerializer,
    ProductDetailSerializer,
    TagSerializer,
    TagConnectorSerializer,
)


# Create your views here.
class ProductList(APIView):
    """List all Products, or create a new Product."""

    serializer_class = SecondaryProductSerializer

    def get(self, request, format=None):
        products = (
            Product.objects.select_related("category")
            .prefetch_related("tagconnector_set__tag")
            .filter()
            .order_by("id")
        )
        name = request.query_params.get("name", "")
        if name:
            products = products.filter(name__icontains=name)

        page = request.query_params.get("page")
        paginator = Paginator(products, 5)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page is None:
            page = 1

        page = int(page)

        serializer = self.serializer_class(products, many=True)
        return Response(
            {"products": serializer.data, "page": page, "pages": paginator.num_pages},
            status.HTTP_200_OK,
        )


class TopProducts(APIView):
    """get all top-rated products"""

    serializer_class = SecondaryProductSerializer

    def get(self, request, format=None):
        products = Product.objects.filter(rating__gte=4).order_by("-rating")[:5]
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class ProductCreate(APIView):
    """Create product by admin user"""

    serializer_class = ProductSerializer

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    """Retrieve a product detail"""

    serializer_class = ProductDetailSerializer

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        product = self.get_object(slug)
        serializer = self.serializer_class(product)
        return Response(serializer.data)


@permission_classes([IsAdminUser])
class ProductUpdateDelete(APIView):
    """Product update and delete by admin"""

    serializer_class = ProductSerializer

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

    permission_classes([IsAdminUser])

    def delete(self, request, slug, format=None):
        product = self.get_object(slug)
        product.delete()
        return Response(
            {"msg": "Product Deleted successfully"}, status.HTTP_204_NO_CONTENT
        )


"""Tag Views"""


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


"""Product Tag Connector Views"""


class TagConnectorList(APIView):
    """List all tag connector, or create a new tag connector."""

    serializer_class = TagConnectorSerializer

    def get(self, request, format=None):
        product_tags = TagConnector.objects.all()
        serializer = self.serializer_class(product_tags, many=True)
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


class TagConnectorDetail(APIView):
    """Retrieve, update or delete a tag connector instance."""

    serializer_class = TagConnectorSerializer

    def get_object(self, pk):
        try:
            return TagConnector.objects.get(pk=pk)
        except TagConnector.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product_tag = self.get_object(pk)
        serializer = self.serializer_class(product_tag)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=serializer_class,
    )
    def put(self, request, pk, format=None):
        product_tag = self.get_object(pk)
        serializer = self.serializer_class(product_tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product_tag = self.get_object(pk)
        product_tag.delete()
        return Response(
            {"msg": "Tag connector Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
