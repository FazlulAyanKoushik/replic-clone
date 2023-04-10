"""
    Test Tag API
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from product.models import Tag
from product.serializers import TagSerializer
from django.contrib.auth import get_user_model

TAG_LIST_URL = reverse('product:tag-list')
TAG_ADD_URL = reverse('product:tag-add')


def tag_detail_url(tag_slug):
    return reverse('product:tag-detail', args=[tag_slug])


def tag_update_url(tag_slug):
    return reverse('product:tag-update', args=[tag_slug])


def tag_delete_url(tag_slug):
    return reverse('product:tag-delete', args=[tag_slug])


def create_tag(**payload):
    return Tag.objects.create(**payload)


class PublicTagTest(TestCase):
    """Testing tag API fail to user"""

    def setUp(self):
        self.client = APIClient()

    def test_tag_list_get_fail(self):
        """Testing get all tag list return fail"""
        tag1 = create_tag(name='tag1')
        tag2 = create_tag(name='tag2')
        tag3 = create_tag(name='tag3')
        response = self.client.get(TAG_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagList(TestCase):
    """Testing tag api for admin user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@example.com', password='test1234')
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_tag_list_get_successfully(self):
        """Testing get all tag list get successfully"""
        tag1 = create_tag(name='tag1')
        tag2 = create_tag(name='tag2')
        tag3 = create_tag(name='tag3')
        response = self.client.get(TAG_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tag(self):
        """Testing tag create successfully"""
        payload = {'name': 'Test Tag'}
        response = self.client.post(TAG_ADD_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get().name, 'Test Tag')

    def test_get_tag(self):
        """Testing tag details get successfully"""
        tag = create_tag(name='tag1')
        url = tag_detail_url(tag.slug)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TagSerializer(tag).data)

    def test_update_tag(self):
        """Testing tag update successfully"""
        tag = create_tag(name='tag1')
        payload = {
            'name': 'Updated Tag'
        }
        url = tag_update_url(tag.slug)
        response = self.client.put(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, 'Updated Tag')

    def test_delete_tag(self):
        """Testing tag delete successfully"""
        tag = create_tag(name='tag1')
        url = tag_delete_url(tag.slug)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())
