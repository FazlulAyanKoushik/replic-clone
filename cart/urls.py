"""
    Urls for Cart
"""
from django.urls import path
from cart import views

app_name = "cart"

urlpatterns = [
    path("", views.CartList.as_view(), name="list"),
    path("", views.CartList.as_view(), name="item"),
]
