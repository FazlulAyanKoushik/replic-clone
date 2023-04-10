"""
    Model for shipping address
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
    address = models.TextField()
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.address)[0:40]
