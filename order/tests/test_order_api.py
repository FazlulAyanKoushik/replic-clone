"""
    Test Order API
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Product
from category.models import Category
from cart.models import Cart
from order.models import Order
from order.serializers import OrderSerializer
from cart.serializers import CartSerializer
from django.contrib.auth import get_user_model

from shipping_address.models import ShippingAddress

User = get_user_model()

"""User Urls"""
ORDER_LIST_URL = reverse("order:list")
ORDER_ADD_URL = reverse("order:add")


def create_shipping_address(**payload):
    return ShippingAddress.objects.create(**payload)


def create_category(**payload):
    """Create and return a category"""
    return Category.objects.create(**payload)


def create_product(**payload):
    return Product.objects.create(**payload)


def create_user(**payload):
    return User.objects.create_user(**payload)


class PrivateOrderTest(TestCase):
    """Test that authenticate user can have the access and can request"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="userpass")
        self.client.force_authenticate(user=self.user)
        self.category = create_category(name="Category")
        self.product = create_product(
            name="Test product", category=self.category, price="10", stock=10
        )
        self.cart1 = Cart.objects.create(
            user=self.user,
            item=self.product,
            quantity=2,
        )
        self.cart2 = Cart.objects.create(
            user=self.user,
            item=self.product,
            quantity=2,
        )
        shipping_address = create_shipping_address(
            user=self.user,
            address="House:114/4, west agargaon",
            city="Dhaka",
            zipcode="1207",
            country="bangladesh",
        )

    def test_create_order(self):
        """Test that authenticated user can create an order"""
        response = self.client.post(ORDER_ADD_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
