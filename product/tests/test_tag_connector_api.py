"""
    Test Tag Connector API
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from category.models import Category
from product.models import Tag, TagConnector, Product
from product.serializers import TagSerializer, TagConnectorSerializer
from django.contrib.auth import get_user_model

TAG_CONNECTOR_LIST_URL = reverse('product:connector-list')
TAG_CONNECTOR_ADD_URL = reverse('product:connector-add')


def tag_connector_detail_url(connector_id):
    return reverse('product:connector-detail', args=[connector_id])


def tag_connector_update_url(connector_id):
    return reverse('product:connector-update', args=[connector_id])


def tag_connector_delete_url(connector_id):
    return reverse('product:connector-delete', args=[connector_id])


def create_tag_connector(**payload):
    return TagConnector.objects.create(**payload)


def create_product(**payload):
    return Product.objects.create(**payload)


def create_tag(**payload):
    return Tag.objects.create(**payload)


class PrivateTagConnectorTests(TestCase):
    """Test that only admin user can access those APIs"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@example.com', password='test1234')
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Test Category")
        self.product = create_product(name='Test product', category=self.category, price="10.00")
        self.tag1 = create_tag(name='tag1')
        self.tag2 = create_tag(name='tag2')

    def test_get_tag_connector_list(self):
        """Test that we can get a list of tag connectors"""
        tag_connector1 = create_tag_connector(product=self.product, tag=self.tag1)
        tag_connector2 = create_tag_connector(product=self.product, tag=self.tag2)
        response = self.client.get(TAG_CONNECTOR_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_tag_connector(self):
        """Test that we can create a new tag connector"""
        payload = {
            'product': self.product.id,
            'tag': self.tag1.id,
        }
        response = self.client.post(TAG_CONNECTOR_ADD_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TagConnector.objects.count(), 1)

    def test_get_tag_connector_detail(self):
        """Test that we can get a tag connector by id"""
        tag_connector = create_tag_connector(product=self.product, tag=self.tag1)
        url = tag_connector_detail_url(tag_connector.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TagConnectorSerializer(tag_connector).data)

    def test_update_tag_connector(self):
        """Test that we can update a tag connector"""
        tag_connector = create_tag_connector(product=self.product, tag=self.tag1)
        payload = {
            'product': self.product.id,
            'tag': self.tag2.id,
        }
        url = tag_connector_update_url(tag_connector.id)
        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag_connector.refresh_from_db()
        self.assertEqual(str(tag_connector.tag), 'tag2')

    def test_delete_tag_connector(self):
        """Test that we can delete a tag connector"""
        tag_connector = create_tag_connector(product=self.product, tag=self.tag1)
        url = tag_connector_delete_url(tag_connector.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TagConnector.objects.filter(id=tag_connector.id).exists())
