"""
    Test Tag Connector model
"""
from django.test import TestCase
from product.models import Tag, Product, TagConnector


class TagConnectorTestCase(TestCase):
    """Testing TagConnector model test"""
    def setUp(self):
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.product = Product.objects.create(
            name='Test Product',
            category=None,
            price=10.00,
            quantity=10,
            description='Test product description',
        )

    def test_tag_connector_creation(self):
        """Testing TagConnector is created successfully"""
        tag_connector1 = TagConnector.objects.create(
            product=self.product,
            tag=self.tag1,
        )
        self.assertEqual(tag_connector1.product, self.product)
        self.assertEqual(tag_connector1.tag, self.tag1)

        tag_connector2 = TagConnector.objects.create(
            product=self.product,
            tag=self.tag2,
        )
        self.assertEqual(tag_connector2.product, self.product)
        self.assertEqual(tag_connector2.tag, self.tag2)

    def test_tag_connector_uniqueness(self):
        """Testing same product and tag not creating twice"""
        tag_connector1 = TagConnector.objects.create(
            product=self.product,
            tag=self.tag1,
        )
        with self.assertRaises(Exception):
            TagConnector.objects.create(
                product=self.product,
                tag=self.tag1,
            )

    def test_tag_connector_str_method(self):
        """Testing tag connector model return expected object str"""
        tag_connector = TagConnector.objects.create(
            product=self.product,
            tag=self.tag1,
        )
        expected_str = f"{self.product.name} - {self.tag1.name}"
        self.assertEqual(str(tag_connector), expected_str)
