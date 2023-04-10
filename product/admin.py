from django.contrib import admin
from product.models import Product, Tag, TagConnector

# Register your models here.

admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(TagConnector)
