"""
    Test review model
"""
from django.test import TestCase
from category.models import Category
from review.models import Review
from product.models import Product
from django.contrib.auth import get_user_model


class ReviewModelTest(TestCase):
    """Testing review model"""

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test product', category=self.category, price="10.00")
        self.user = get_user_model().objects.create_user(email='test@example.com', password='test1234')

    def test_review_add(self):
        """testing  add review"""
        review = Review.objects.create(user=self.user, name=self.user.email, product=self.product, rating=4, comment='Test comment')
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, 'Test comment')
