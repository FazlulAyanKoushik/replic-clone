"""
    Test Order API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from cart.models import Cart
from category.models import Category
from order.models import Order
from order.serializers import OrderSerializer
from product.models import Product
from shipping_address.models import ShippingAddress

User = get_user_model()

"""User Order Urls"""
ORDER_LIST_URL = reverse("order:list")
ORDER_ADD_URL = reverse("order:add")


def order_detail(order_uuid):
    return reverse("order:detail", args=[order_uuid])


"""Admin Order Urls"""
ADMIN_ORDER_LIST_URLS = reverse("order:items-admin")


def admin_order_detail_by_uuid(order_uuid):
    return reverse("order:detail-admin", args=[order_uuid])


def admin_order_delete_by_uuid(order_uuid):
    return reverse("order:delete-admin", args=[order_uuid])


def admin_update_order_to_paid(order_uuid):
    return reverse("order:order-paid-admin", args=[order_uuid])


def admin_update_order_to_delivered(order_uuid):
    return reverse("order:order-delivered-admin", args=[order_uuid])


def create_shipping_address(**payload):
    return ShippingAddress.objects.create(**payload)


def create_category(**payload):
    """Create and return a category"""
    return Category.objects.create(**payload)


def create_product(**payload):
    return Product.objects.create(**payload)


def create_user(**payload):
    return User.objects.create_user(**payload)


def create_super_user(**payload):
    return User.objects.create_superuser(**payload)


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
        self.shipping_address = create_shipping_address(
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
        self.assertEqual(len(response.data["order_items"]), 2)

    def test_user_order_list(self):
        """Test that user gets an order list"""
        res = self.client.post(ORDER_ADD_URL)

        # Get an order list as response
        response = self.client.get(ORDER_LIST_URL)

        self.assertEqual(len(response.data), 1)
        orders = Order.objects.filter(user=self.user)
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_user_order_detail(self):
        """Test that User gets order detail"""
        order = self.client.post(ORDER_ADD_URL)
        url = order_detail(order.data["uuid"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = Order.objects.get(uuid=order.data["uuid"])
        serializer = OrderSerializer(order)

        self.assertEqual(response.data, serializer.data)


"""ADin Order Test"""


class SuperPrivateOrderTest(TestCase):
    """Test that only admin user can access these APIs"""

    def setUp(self):
        self.client = APIClient()
        self.superuser = create_super_user(
            email="admin@example.com", password="userpass"
        )
        self.client.force_authenticate(user=self.superuser)
        self.user1 = create_user(email="user1@example.com", password="userpass")
        self.user2 = create_user(email="use2@example.com", password="userpass")
        self.category = create_category(name="Category")
        self.product = create_product(
            name="Test product", category=self.category, price="10", stock=10
        )
        self.cart1 = Cart.objects.create(
            user=self.user1,
            item=self.product,
            quantity=2,
        )
        self.cart2 = Cart.objects.create(
            user=self.user1,
            item=self.product,
            quantity=2,
        )
        self.shipping_address1 = create_shipping_address(
            user=self.user1,
            address="House:114/4, west Agargaon",
            city="Dhaka",
            zipcode="1207",
            country="bangladesh",
        )
        self.cart2 = Cart.objects.create(
            user=self.user2,
            item=self.product,
            quantity=2,
        )
        self.cart3 = Cart.objects.create(
            user=self.user2,
            item=self.product,
            quantity=2,
        )
        self.shipping_address2 = create_shipping_address(
            user=self.user2,
            address="House:114/4, west Agargaon",
            city="Dhaka",
            zipcode="1207",
            country="bangladesh",
        )
        self.order1 = Order.objects.create(
            user=self.user1,
            shipping_address=self.shipping_address1,
            total_price="100",
        )
        carts_1 = Cart.objects.filter(user=self.user1)
        self.order1.order_items.set(carts_1)
        self.order1.save()

        self.order2 = Order.objects.create(
            user=self.user2,
            shipping_address=self.shipping_address2,
            total_price="100",
        )
        carts_2 = Cart.objects.filter(user=self.user2)
        self.order1.order_items.set(carts_2)
        self.order2.save()

    def test_get_all_orders(self):
        """Test that admin have all user order list"""

        response = self.client.get(ADMIN_ORDER_LIST_URLS)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        orders = Order.objects.filter()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_admin_order_detail_by_uuid(self):
        """Test that admin can get specific order detail by order uuid"""
        url = admin_order_detail_by_uuid(self.order1.uuid)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = OrderSerializer(self.order1)
        self.assertEqual(response.data, serializer.data)

    def test_admin_delete_order_by_uuid(self):
        """Test that admin can delete a specific order by order uuid"""

        url = admin_order_delete_by_uuid(self.order2.uuid)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_update_order_to_paid(self):
        """Test that admin can change the status of order as paid"""
        url = admin_update_order_to_paid(self.order1.uuid)

        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order1.refresh_from_db()

        self.assertEqual(self.order1.is_paid, True)

    def test_admin_update_order_to_delivered(self):
        """Test that admin can change the status of order as delivered"""
        url = admin_update_order_to_delivered(self.order1.uuid)

        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order1.refresh_from_db()

        self.assertEqual(self.order1.is_delivered, True)
