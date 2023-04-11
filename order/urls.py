"""
    Urls for Order
"""
from django.urls import path
from order import views

app_name = "order"

urlpatterns = [
    path("list/", views.OrderList.as_view(), name="list"),
    path("add/", views.OrderList.as_view(), name="add"),
]
