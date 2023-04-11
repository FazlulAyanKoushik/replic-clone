"""
    Test for shipping address
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shipping_address.models import ShippingAddress
from shipping_address.serializers import ShippingAddressSerializer

User = get_user_model()

SHIPPING_ADDRESS_ADD_URL = reverse("shipping_address:add")
SHIPPING_ADDRESS_DETAIL_URL = reverse("shipping_address:detail")
SHIPPING_ADDRESS_UPDATE_URL = reverse("shipping_address:update")
SHIPPING_ADDRESS_DELETE_URL = reverse("shipping_address:delete")


def create_user(**payload):
    return User.objects.create_user(**payload)


def create_shipping_address(**payload):
    return ShippingAddress.objects.create(**payload)


class PrivateShippingAddress(TestCase):
    """Test that only authenticated user can access these APIs"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="userpass")
        self.client.force_authenticate(user=self.user)

    def test_create_shipping_address(self):
        """Test that authenticated user can create a shipping address"""
        payload = {
            "address": "House:114/4, west agargaon",
            "city": "Dhaka",
            "zipcode": "1207",
            "country": "bangladesh",
        }
        response = self.client.post(SHIPPING_ADDRESS_ADD_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_shipping_address_detail(self):
        """Test that shipping address details get perfectly"""
        shipping_address = create_shipping_address(
            user=self.user,
            address="House:114/4, west agargaon",
            city="Dhaka",
            zipcode="1207",
            country="bangladesh",
        )
        response = self.client.get(SHIPPING_ADDRESS_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        my_address = ShippingAddress.objects.get(user=self.user)
        serializer = ShippingAddressSerializer(my_address)
        self.assertEqual(response.data, serializer.data)

    def test_shipping_address_update(self):
        """Test that shipping address details get perfectly"""
        shipping_address = create_shipping_address(
            user=self.user,
            address="House:114/4, west agargaon",
            city="Dhaka",
            zipcode="1207",
            country="bangladesh",
        )
        payload = {
            "address": "House:114/4, west agargaon",
            "city": "Chittagong",
            "zipcode": "1507",
            "country": "bangladesh",
        }
        response = self.client.get(SHIPPING_ADDRESS_UPDATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shipping_address.refresh_from_db()
        my_address = ShippingAddress.objects.get(user=self.user)
        serializer = ShippingAddressSerializer(my_address)
        self.assertEqual(response.data, serializer.data)

    def test_shipping_address_delete(self):
        """Test that shipping address details get perfectly"""
        shipping_address = create_shipping_address(
            user=self.user,
            address="House:114/4, west agargaon",
            city="Dhaka",
            zipcode="1207",
            country="bangladesh",
        )
        response = self.client.delete(SHIPPING_ADDRESS_DELETE_URL)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
