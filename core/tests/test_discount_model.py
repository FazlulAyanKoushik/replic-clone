"""
    Testing discount model
"""
from decimal import Decimal
from django.test import TestCase
from category.models import Category, Discount


class DiscountModelTestCase(TestCase):
    """Testing Discount model"""
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.discount = Discount.objects.create(
            name='Test Discount',
            category=self.category,
            percentage=10.50,
        )

    def test_discount_name(self):
        """Testing discount model returning expected str"""
        self.assertEqual(str(self.discount), 'test-discount')

    def test_discount_category(self):
        """Testing discount category"""
        self.assertEqual(self.discount.category, self.category)

    def test_discount_percentage(self):
        """Testing discount percentage amount"""
        self.assertEqual(self.discount.percentage, Decimal('10.50'))
