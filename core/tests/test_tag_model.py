"""
    Test Tag model
"""
from django.test import TestCase
from product.models import Tag


class TagTestCase(TestCase):
    """Testing tag model"""
    def setUp(self):
        self.tag1 = Tag.objects.create(name='Tag1')
        self.tag2 = Tag.objects.create(name='Tag2')
        self.tag3 = Tag.objects.create(name='Tag3')

    def test_str_method(self):
        """Testing tag model return expected object str"""
        self.assertEqual(str(self.tag1), 'tag1')
        self.assertEqual(str(self.tag2), 'tag2')
        self.assertEqual(str(self.tag3), 'tag3')

    def test_slug_field(self):
        """Testing tag model slug working successfully"""
        self.assertEqual(self.tag1.slug, 'tag1')
        self.assertEqual(self.tag2.slug, 'tag2')
        self.assertEqual(self.tag3.slug, 'tag3')
