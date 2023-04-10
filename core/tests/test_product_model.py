"""
    Test product model
"""
from django.test import TestCase
from product.models import Category
from product.models import Product
from django.contrib.auth import get_user_model


class ProductModelTest(TestCase):
    """Testing product model"""

    def setUp(self):
        self.category = Category.objects.create(name='Test category')

    def test_create_product_successfully(self):
        """Testing creating a product by admin successfully"""
        product_name = 'Test Product'
        category = self.category
        price = "10.00"

        product = Product.objects.create(
            name=product_name,
            category=category,
            price=price
        )

        self.assertEqual(product.name, product_name)
        self.assertEqual(product.category, category)
        self.assertEqual(product.price, price)
        self.assertEqual(product.slug, 'test-product')

