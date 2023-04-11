"""
    Urls for Cart
"""
from django.urls import path
from shipping_address import views

app_name = "shipping_address"

urlpatterns = [
    path("add/", views.CreateShippingAddress.as_view(), name="add"),
    path("detail/", views.ShippingAddressDetail.as_view(), name="detail"),
    path("update/", views.ShippingAddressDetail.as_view(), name="update"),
    path("delete/", views.ShippingAddressDetail.as_view(), name="delete"),
]
