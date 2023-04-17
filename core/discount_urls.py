"""
    Urls for Admin users
"""
from django.urls import path
from core import views

app_name = "admin-discount"

urlpatterns = [
    # Discounts urls
    path("", views.DiscountList.as_view(), name="discount-list"),
    path("", views.DiscountList.as_view(), name="discount-add"),
    path(
        "<str:slug>",
        views.DiscountDetail.as_view(),
        name="discount-detail",
    ),
    path(
        "<str:slug>",
        views.DiscountDetail.as_view(),
        name="discount-update",
    ),
    path(
        "<str:slug>",
        views.DiscountDetail.as_view(),
        name="discount-delete",
    ),
]
