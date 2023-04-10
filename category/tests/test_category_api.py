"""
    Test for category API
"""
from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from decimal import Decimal
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from category.models import Category
from category.serializers import CategorySerializer
from product.models import Product

CATEGORY_LIST_URL = reverse('category:category-list')
CATEGORY_ADD_URL = reverse('category:category-add')


def create_user(**payload):
    """Create and return a user"""
    return get_user_model().objects.create_user(**payload)


def category_detail_url(slug):
    """category retrieve url"""
    return reverse('category:category-detail', args=[slug])


def category_update_url(slug):
    """category update url"""
    return reverse('category:category-update', args=[slug])


def category_delete_url(slug):
    """category delete url"""
    return reverse('category:category-delete', args=[slug])


def create_category(**payload):
    """Create and return a category"""
    return Category.objects.create(**payload)


def category_products(slug):
    """category related products url"""
    return reverse('category:category-products', args=[slug])


class PublicCategoryTest(TestCase):
    """Test unauthenticated category API request"""

    def setUp(self):
        self.client = APIClient()

    def test_get_all_category_list(self):
        """Testing that we can get a list of all categories."""
        create_category(name='category-1')
        create_category(name='category-2')
        create_category(name='category-3')

        res = self.client.get(CATEGORY_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)
        categories = Category.objects.filter()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_category_as_non_admin(self):
        """Test that a non-admin user cannot create a new category."""
        payload = {
            "name": "test category"
        }
        res = self.client.post(CATEGORY_ADD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_category_by_user(self):
        """Testing retrieve category by unauthenticated user"""
        category = create_category(name='category-1')
        url = category_detail_url(category.slug)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        my_category = Category.objects.get(slug=category.slug)
        serializer = CategorySerializer(my_category)
        self.assertEqual(res.data, serializer.data)

    def test_get_product_by_category_slug(self):
        """Testing get all related products of category"""
        category_1 = create_category(name='category-1')
        category_2 = create_category(name='category-2')
        product_1 = Product.objects.create(name='product-1', category=category_1, price="20.00")
        product_2 = Product.objects.create(name='product-2', category=category_1, price="20.00")
        product_3 = Product.objects.create(name='product-3', category=category_2, price="20.00")

        url = category_products(category_1.slug)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)


class PrivateCategoryTest(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='admin@example.com',
            password='test1234',
        )
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_category_as_admin(self):
        """Test that an admin can create a new category."""
        payload = {
            'name': 'Test Category'
        }
        res = self.client.post(CATEGORY_ADD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_create_category_with_invalid_data(self):
        """Test that we cannot create a category with invalid data."""
        payload = {
            'name': ' '
        }
        res = self.client.post(CATEGORY_ADD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_category_by_admin(self):
        # test updating a category by admin user
        category = create_category(name='category-1')
        payload = {
            'name': 'updated-category'
        }
        url = category_update_url(category.slug)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        my_category = Category.objects.get(slug=category.slug)
        serializer = CategorySerializer(my_category)
        self.assertEqual(res.data, serializer.data)

    def test_delete_category_by_admin_user(self):
        # test deleting a category by admin user
        category = create_category(name='category-1')
        url = category_delete_url(category.slug)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(slug=category.slug))
