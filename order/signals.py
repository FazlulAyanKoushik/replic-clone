"""
    Signal for the Order model
"""
from random import randint

from django.db.models.signals import pre_save
from django.dispatch import receiver

from order.models import Order


@receiver(pre_save, sender=Order)
def generate_order_id(sender, instance, **kwargs):
    """
    A signal receiver to generate a unique order_id before saving the Order instance.
    """
    if not instance.order_id:
        while True:
            # Generate a random 6-digit integer for order_id
            order_id = randint(100000, 999999)
            # Check if order_id is unique
            if not Order.objects.filter(order_id=order_id).exists():
                instance.order_id = order_id
                break
