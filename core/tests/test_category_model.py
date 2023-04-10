"""
    Test category model
"""
from django.test import TestCase
from category.models import Category
from decimal import Decimal


class CategoryModelTest(TestCase):
    """Testing category model"""

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_slug(self):
        """Testing that the slug is automatically generated when the Category is saved."""
        self.assertEqual(self.category.slug, 'test-category')

