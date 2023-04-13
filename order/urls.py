"""
    Urls for Order
"""
from django.urls import path
from order import views

app_name = "order"

urlpatterns = [
    # Admin order urls
    path("admin", views.AdminOrderList.as_view(), name="items-admin"),
    path(
        "admin/<str:uuid>",
        views.AdminOrderDetail.as_view(),
        name="detail-admin",
    ),
    path(
        "admin/<str:uuid>",
        views.AdminOrderDetail.as_view(),
        name="delete-admin",
    ),
    path(
        "admin/paid/<str:uuid>",
        views.UpdateOrderToPaid.as_view(),
        name="order-paid-admin",
    ),
    path(
        "admin/delivered/<str:uuid>",
        views.UpdateOrderToDelivered.as_view(),
        name="order-delivered-admin",
    ),
    # Orders Urls
    path("", views.OrderList.as_view(), name="list"),
    path("", views.OrderList.as_view(), name="add"),
    path("<str:uuid>", views.OrderDetail.as_view(), name="detail"),
]
