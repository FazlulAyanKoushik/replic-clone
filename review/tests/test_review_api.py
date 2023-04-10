"""
    Test review API
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from product.models import Product
from category.models import Category
from review.models import Review
from django.contrib.auth import get_user_model


def review_add_url(product_slug):
    return reverse('review:add-review', args=[product_slug])


class PublicReviewTest(TestCase):
    """Testing reviews by unauthenticated user"""

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test product', category=self.category, price="10.00")
        self.user = get_user_model().objects.create_user(email='test@example.com', password='test1234')
        self.client = APIClient()

    def test_review_with_unauthenticated_user(self):
        """testing raise error if unauthenticated user try to add review"""
        url = review_add_url(self.product.slug)
        payload = {
            'user': self.user,
            'product': self.product,
            'name': self.user.email,
            'rating': 4,
            'comment': 'Great Product'
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReviewTest(TestCase):
    """Test review for authenticate user"""

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test product', category=self.category, price="10.00")
        self.product2 = Product.objects.create(name='Test product2', category=self.category, price="10.00")
        self.user = get_user_model().objects.create_user(email='test@example.com', password='test1234')
        self.client.force_authenticate(user=self.user)

    def test_create_product_review_api(self):
        """Testing create product review successfully"""
        payload = {
            'user': self.user,
            'product': self.product,
            'name': self.user.email,
            'rating': 4,
            'comment': 'Great Product'
        }
        url = review_add_url(self.product.slug)
        res = self.client.post(url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['msg'], 'Review added')

    def test_create_review_with_existing_review(self):
        """Test creating a review with an already existing review"""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            name=self.user.email,
            rating=4,
            comment='Great Product'
        )

        url = review_add_url(self.product.slug)
        payload = {
            'user': self.user,
            'product': self.product,
            'name': self.user.email,
            'rating': 4,
            'comment': 'Great Product'
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['msg'], 'Product already reviewed')

        reviews = Review.objects.filter(product=self.product)
        self.product.refresh_from_db()
        self.assertEqual(self.product.review_set.count(), 1)

    def test_create_review_with_rating_zero(self):
        """Test creating a review with rating 0"""
        payload1 = {
            'user': self.user,
            'product': self.product2,
            'name': self.user.email,
            'rating': 0,
            'comment': 'Great Product'
        }
        url = review_add_url(self.product2.slug)
        res = self.client.post(url, payload1)
    #
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['msg'], 'Please select a minimum rating')
        reviews = Review.objects.filter(product=self.product)
        self.product.refresh_from_db()
        self.assertEqual(self.product.review_set.count(), 0)
