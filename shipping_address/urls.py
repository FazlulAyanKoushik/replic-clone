"""
    Urls for Cart
"""
from django.urls import path
from shipping_address import views

app_name = "shipping_address"

urlpatterns = [
    path("", views.CreateShippingAddress.as_view(), name="add"),
    path("user/", views.ShippingAddressDetail.as_view(), name="detail"),
    path("user/", views.ShippingAddressDetail.as_view(), name="update"),
    path("user/", views.ShippingAddressDetail.as_view(), name="delete"),
]
