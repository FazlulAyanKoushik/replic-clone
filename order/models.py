"""
    Model for Order
"""
from django.contrib.auth import get_user_model
from django.db import models

from cart.models import Cart
from core.models import BaseModel
from shipping_address.models import ShippingAddress

User = get_user_model()


class Order(BaseModel):
    order_id = models.PositiveIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_items = models.ManyToManyField(Cart)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    delivery_charge = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Order Id: {{self.order_id}}, Customer: {{self.user}}, - Total: {{self.total_price}}"
