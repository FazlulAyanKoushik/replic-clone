"""
    Test Cart APIs
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from product.models import Product
from category.models import Category
from cart.models import Cart
from cart.serializers import CartSerializer
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

CART_LIST_URL = reverse('cart:list')
CART_ITEM_URL = reverse('cart:item')


def create_user(**payload):
    return User.objects.create_user(**payload)


def create_category(**payload):
    """Create and return a category"""
    return Category.objects.create(**payload)


def create_product(**payload):
    return Product.objects.create(**payload)


class PrivateCartTest(TestCase):
    """Test that only authenticate user can access cart"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='userpass')
        self.category = create_category(name='Category')
        self.client.force_authenticate(user=self.user)

    def test_get_cart(self):
        """Test getting cart"""
        product1 = create_product(
            name='Test product',
            category=self.category,
            price="10.00",
            discount_price="5",
            stock=10
        )
        product2 = create_product(
            name='Test product2',
            category=self.category,
            price="10.00",
            stock=10
        )
        cart1 = Cart.objects.create(user=self.user, item=product1, quantity=3)
        cart2 = Cart.objects.create(user=self.user, item=product2, quantity=2)
        response = self.client.get(CART_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        carts = Cart.objects.filter(user=self.user)
        serializer = CartSerializer(carts, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_add_to_cart(self):
        """Test adding an item to the cart"""
        product = create_product(
            name='Test product',
            category=self.category,
            price="10.00",
            discount_price="5",
            stock=10
        )
        payload = {
            "product_slug": product.slug,
            "quantity": 2,
            "action": "inc"
        }
        response = self.client.post(CART_ITEM_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = Cart.objects.get(user=self.user, item=product)
        serializer = CartSerializer(cart)
        self.assertEqual(response.data, serializer.data)
        product.refresh_from_db()
        self.assertEqual(product.stock, 8)

    def test_remove_from_cart(self):
        """Test adding an item to the cart"""
        product = create_product(
            name='Test product',
            category=self.category,
            price="10.00",
            discount_price="5",
            stock=10
        )
        cart = Cart.objects.create(user=self.user, item=product, quantity=3)
        payload = {
            "product_slug": product.slug,
            "quantity": 2,
            "action": "dec"
        }
        response = self.client.post(CART_ITEM_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = Cart.objects.get(user=self.user, item=product)
        serializer = CartSerializer(cart)
        self.assertEqual(response.data, serializer.data)
        product.refresh_from_db()
        self.assertEqual(product.stock, 12)

    def test_cart_with_product_discount_price(self):
        """Test adding an item to the cart with a discount price"""
        product = create_product(
            name='Test product',
            category=self.category,
            price="10.00",
            discount_price="5",
            stock=10
        )
        payload = {
            "product_slug": product.slug,
            "quantity": 2,
            "action": "inc"
        }
        response = self.client.post(CART_ITEM_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_price'], Decimal('10.00'))

