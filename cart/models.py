"""
    model for Cart
"""
from django.db import models
from core.models import BaseModel
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_carts')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        if self.item.discount_price:
            return self.item.discount_price * self.quantity
        else:
            return self.item.price * self.quantity

    def __str__(self):
        return f"Customer :{{self.user}}, - Item: {{self.item.name}}"
