"""
    Urls for Order
"""
from django.urls import path
from order import views

app_name = "order"

urlpatterns = [
    path("list/", views.OrderList.as_view(), name="list"),
    path("add/", views.OrderList.as_view(), name="add"),
    path("detail/<str:uuid>/", views.OrderDetail.as_view(), name="detail"),
    # Admin order urls
    path("items/admin/", views.AdminOrderList.as_view(), name="items-admin"),
    path(
        "detail/admin/<str:uuid>/",
        views.AdminOrderDetail.as_view(),
        name="detail-admin",
    ),
    path(
        "delete/admin/<str:uuid>/",
        views.AdminOrderDetail.as_view(),
        name="delete-admin",
    ),
    path(
        "paid/admin/<str:uuid>/",
        views.UpdateOrderToPaid.as_view(),
        name="order-paid-admin",
    ),
    path(
        "delivered/admin/<str:uuid>/",
        views.UpdateOrderToDelivered.as_view(),
        name="order-delivered-admin",
    ),
]
