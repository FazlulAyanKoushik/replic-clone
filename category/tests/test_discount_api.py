"""
    Test for discount API
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category, Discount
from product.models import Product

User = get_user_model()

DISCOUNT_LIST_URL = reverse("admin-discount:discount-list")
DISCOUNT_ADD_URL = reverse("admin-discount:discount-add")


def discount_detail(discount_slug):
    return reverse("admin-discount:discount-detail", args=[discount_slug])


def discount_update(discount_slug):
    return reverse("admin-discount:discount-update", args=[discount_slug])


def discount_delete(discount_slug):
    return reverse("admin-discount:discount-delete", args=[discount_slug])


def create_discount(**payload):
    return Discount.objects.create(**payload)


def create_super_user(**payload):
    return User.objects.create_superuser(**payload)


def create_category(**payload):
    """Create and return a category"""
    return Category.objects.create(**payload)


def create_product(**payload):
    return Product.objects.create(**payload)


class PrivateDiscountTest(TestCase):
    """Test admin has access all these discount API and working"""

    def setUp(self):
        self.client = APIClient()
        self.superuser = create_super_user(
            email="admin@example.com", password="userpass"
        )
        self.client.force_authenticate(user=self.superuser)
        self.category1 = create_category(name="Electronic")
        self.category2 = create_category(name="Food")
        self.product1 = create_product(
            name="Mouse", category=self.category1, price="500", stock=10
        )
        self.product2 = create_product(
            name="KeyBoard", category=self.category1, price="800", stock=10
        )
        self.product3 = create_product(
            name="Laptop", category=self.category1, price="1000", stock=10
        )
        self.product4 = create_product(
            name="Mango", category=self.category2, price="100", stock=10
        )

    def test_create_discount(self):
        """Test that admin can create a discount and working"""
        payload = {
            "name": "Eid offer",
            "category": self.category1.id,
            "percentage": "10",
        }

        response = self.client.post(DISCOUNT_ADD_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product1.refresh_from_db()

        self.assertEqual(self.product1.discount_price, Decimal("450.00"))

    def test_discount_list(self):
        """Test get all discount list"""
        payload = {
            "name": "Eid ul fitter offer",
            "category": self.category1.id,
            "percentage": "10",
        }
        discount1 = self.client.post(DISCOUNT_ADD_URL, payload)

        payload = {
            "name": "Eid ul Ada offer",
            "category": self.category2.id,
            "percentage": "10",
        }
        discount2 = self.client.post(DISCOUNT_ADD_URL, payload)

        response = self.client.get(DISCOUNT_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_discount_detail(self):
        """Test that admin can get discount details by slug"""
        payload = {
            "name": "Eid ul fitter offer",
            "category": self.category1.id,
            "percentage": "10",
        }
        discount1 = self.client.post(DISCOUNT_ADD_URL, payload)

        payload = {
            "name": "Eid ul Ada offer",
            "category": self.category2.id,
            "percentage": "10",
        }
        discount2 = self.client.post(DISCOUNT_ADD_URL, payload)

        url = discount_detail(discount1.data["slug"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_discount_update(self):
        """Test that admin can update discount by slug"""
        payload = {
            "name": "Eid ul fitter offer",
            "category": self.category1.id,
            "percentage": "10",
        }
        discount1 = self.client.post(DISCOUNT_ADD_URL, payload)

        payload = {
            "name": "Eid Offer",
            "category": self.category1.id,
            "percentage": "10",
        }

        url = discount_update(discount1.data["slug"])
        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        discount = Discount.objects.get(slug=discount1.data["slug"])
        self.assertEqual(discount.name, "Eid Offer")

    def test_discount_delete(self):
        """Test that admin can delete discount by slug"""
        payload = {
            "name": "Eid ul fitter offer",
            "category": self.category1.id,
            "percentage": "10",
        }
        discount1 = self.client.post(DISCOUNT_ADD_URL, payload)

        url = discount_delete(discount1.data["slug"])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
