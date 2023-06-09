"""
    Serializer for product
"""
from rest_framework import serializers

from category.models import Category
from category.serializers import CategorySerializer
from product.models import Product, Tag, TagConnector


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class TagConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagConnector
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category = Category.objects.get(id=category_data.id)
        product = Product.objects.create(category=category, **validated_data)
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.category = validated_data.get("category", instance.category)
        instance.image = validated_data.get("image", instance.image)
        instance.price = validated_data.get("price", instance.price)
        instance.description = validated_data.get("description", instance.description)
        instance.stock = validated_data.get("stock", instance.stock)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.numReview = validated_data.get("numReview", instance.numReview)
        instance.discount_price = validated_data.get(
            "discount_price", instance.discount_price
        )
        instance.save()
        return instance


class ProductsSerializer(serializers.ModelSerializer):
    tags_slugs = serializers.ListField(
        # child=serializers.SlugField(),
        write_only=True
    )
    # tags = serializers.StringRelatedField(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "category",
            "tags",
            "tags_slugs",
            "image",
            "price",
            "description",
            "stock",
            "rating",
            "numReview",
            "discount_price",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        tags_data = validated_data.pop("tags_slugs", [])
        tags = []
        for tag_slug in tags_data:
            print("tag slug", tag_slug)
            tag, _ = Tag.objects.get_or_create(slug=tag_slug)
            tags.append(tag)

        product = Product.objects.create(**validated_data)
        product.tags.set(tags)
        return product

    def update(self, instance, validated_data):
        print("Validated Data :", validated_data)
        tags_data = validated_data.pop("tags_slugs", [])
        tags = []
        for tag_slug in tags_data:
            tag, _ = Tag.objects.get_or_create(slug=tag_slug)
            tags.append(tag)

        instance.name = validated_data.get("name", instance.name)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.category = validated_data.get("category", instance.category)
        instance.price = validated_data.get("price", instance.price)
        instance.description = validated_data.get("description", instance.description)
        instance.stock = validated_data.get("stock", instance.stock)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.numReview = validated_data.get("numReview", instance.numReview)
        instance.discount_price = validated_data.get(
            "discount_price", instance.discount_price
        )

        instance.tags.set(tags)
        instance.save()

        return instance


class TagConnectorThroughSerializer(serializers.Serializer):
    slug = serializers.SlugField(source="tag.slug")
    name = serializers.SlugField(source="tag.name")


class SecondaryProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagConnectorThroughSerializer(
        read_only=True, source="tagconnector_set", many=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "image",
            "price",
            "stock",
            "rating",
            "numReview",
            "tags",
            "discount_price",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        exclude = ["id"]


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "slug", "image", "price", "discount_price"]
