"""
    Serializer for category, Discount
"""
from rest_framework import serializers
from category.models import Category, Discount
from product.models import Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'name', 'slug', 'category', 'percentage']

    def create(self, validated_data):
        category = validated_data.get('category')

        # Check if a discount with the same category already exists
        existing_discount = Discount.objects.filter(category=category)
        if existing_discount.exists():
            raise serializers.ValidationError('A discount for this category already exists')

        # Create the new discount
        discount = Discount.objects.create(**validated_data)

        # Apply the discount to all products in the same category
        products = Product.objects.filter(category=discount.category)
        for product in products:
            product.discount_price = 0
            product.discount_price = product.price * (1 - discount.percentage / 100)
            if int(discount.percentage) == 0:
                product.discount_price = None
            product.save()
        return discount

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.category = validated_data.get('category', instance.category)
        instance.percentage = validated_data.get('percentage', instance.percentage)
        instance.save()

        products = Product.objects.filter(category=instance.category)
        for product in products:
            product.discount_price = product.price * (1 - instance.percentage / 100)
            if int(instance.percentage) == 0:
                product.discount_price = None
            product.save()

        return instance

