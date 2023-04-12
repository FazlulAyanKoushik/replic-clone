"""
    Models for product, Tag, TagConnector
"""
from autoslug import AutoSlugField
from django.db import models

from category.models import Category, Discount


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    numReview = models.IntegerField(blank=True, null=True, default=0)
    discount_price = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_discount_price(self):
        """
        Calculates the discount price for the product based on the associated discount.
        """
        if self.discount_price is not None:
            # Discount price is already set, do not recalculate
            return self.discount_price
        if self.category is None:
            # Cannot apply discount without a category
            return None
        try:
            discount = Discount.objects.get(category=self.category)
        except Discount.DoesNotExist:
            # No discount for this category
            return None
        discount_price = self.price * (1 - discount.percentage / 100)
        self.discount_price = discount_price
        return discount_price

    def __str__(self):
        return self.slug


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)

    def __str__(self):
        return self.slug


class TagConnector(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "tag")

    def __str__(self):
        return str(self.product.name) + " - " + str(self.tag.name)
