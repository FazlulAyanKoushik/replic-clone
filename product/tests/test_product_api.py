"""
    Test Product API
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from product.models import Product
from product.serializers import ProductSerializer, ProductDetailSerializer
from category.models import Category
from django.contrib.auth import get_user_model

PRODUCT_LIST_URL = reverse("product:list")
PRODUCT_TOP_URL = reverse("product:top-rated")
PRODUCT_ADD_URL = reverse("product:create")


def product_detail_url(product_slug):
    return reverse("product:detail", args=[product_slug])


def product_update_url(product_slug):
    return reverse("product:update", args=[product_slug])


def product_delete_url(product_slug):
    return reverse("product:delete", args=[product_slug])


def create_product(**payload):
    return Product.objects.create(**payload)


class PublicProductTest(TestCase):
    """Testing product APIs for all user"""

    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.client = APIClient()

    def test_Product_list_get_successfully(self):
        """Testing gets all product lists with pagination"""

        product1 = create_product(
            name="Test product", category=self.category, price="10.00"
        )
        product2 = create_product(
            name="Test product", category=self.category, price="10.00"
        )
        product3 = create_product(
            name="Test product", category=self.category, price="10.00"
        )
        product4 = create_product(
            name="Test product", category=self.category, price="10.00"
        )
        product5 = create_product(
            name="Test product", category=self.category, price="10.00"
        )
        product6 = create_product(
            name="Test product", category=self.category, price="10.00"
        )
        product7 = create_product(
            name="Test product", category=self.category, price="10.00"
        )

        res = self.client.get(PRODUCT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["products"]), 5)

    def test_top_products_get_successfully(self):
        """Testing top products get successfully"""
        product1 = create_product(
            name="Test product", category=self.category, price="10.00", rating="4.50"
        )
        product2 = create_product(
            name="Test product", category=self.category, price="10.00", rating="4.50"
        )
        product3 = create_product(
            name="Test product", category=self.category, price="10.00", rating="4.50"
        )
        product4 = create_product(
            name="Test product", category=self.category, price="10.00", rating="4.00"
        )
        product5 = create_product(
            name="Test product", category=self.category, price="10.00", rating="3.50"
        )
        product6 = create_product(
            name="Test product", category=self.category, price="10.00", rating="2.50"
        )
        product7 = create_product(
            name="Test product", category=self.category, price="10.00", rating="3.50"
        )

        res = self.client.get(PRODUCT_TOP_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)

    def test_product_detail_successfully(self):
        """Testing detail product successfully"""
        product = create_product(
            name="Papaya", category=self.category, price="10.00", rating="4.50"
        )
        url = product_detail_url(product.slug)

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product = Product.objects.get(slug=res.data["slug"])
        serializer = ProductDetailSerializer(product)
        self.assertEqual(res.data, serializer.data)


class PrivateProductTest(TestCase):
    """Testing Product for Authenticate User"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="test1234"
        )
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Test Category")

    def test_product_create_successfully(self):
        """Testing creates product successfully by admin user"""
        payload = {
            "name": "Test product",
            "category": self.category.id,
            "price": "10.00",
        }

        res = self.client.post(PRODUCT_ADD_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(slug=res.data["slug"])
        serializer = ProductSerializer(product)
        self.assertEqual(res.data, serializer.data)

    def test_product_update_successfully(self):
        """Testing update product successfully by admin user"""
        product = create_product(
            name="Papaya", category=self.category, price="10.00", rating="4.50"
        )
        payload = {
            "name": "Test product",
            "category": self.category.id,
            "price": "20.00",
        }
        url = product_update_url(product.slug)

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product = Product.objects.get(slug=res.data["slug"])
        serializer = ProductSerializer(product)
        self.assertEqual(res.data, serializer.data)

    def test_product_delete_successfully(self):
        """Testing update product successfully by admin user"""
        product = create_product(
            name="Papaya", category=self.category, price="10.00", rating="4.50"
        )

        url = product_delete_url(product.slug)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
