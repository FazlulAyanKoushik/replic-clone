"""
    Urls for Category app
"""
from django.urls import path
from category import views

app_name = "category"

urlpatterns = [
    path("", views.CategoryList.as_view(), name="category-list"),
    path("add/", views.CategoryCreate.as_view(), name="category-add"),
    path("detail/<str:slug>/", views.CategoryDetail.as_view(), name="category-detail"),
    path(
        "<str:slug>/",
        views.CategoryUpdateDelete.as_view(),
        name="category-update",
    ),
    path(
        "<str:slug>/",
        views.CategoryUpdateDelete.as_view(),
        name="category-delete",
    ),
    path(
        "products/<str:slug>/",
        views.CategoryProductsBySlug.as_view(),
        name="category-products",
    ),
    # Discount urls
    path("i/discounts/", views.DiscountList.as_view(), name="discount-list"),
    path("i/discounts/", views.DiscountList.as_view(), name="discount-add"),
    path(
        "discounts/<str:slug>/",
        views.DiscountDetail.as_view(),
        name="discount-detail",
    ),
    path(
        "discounts/<str:slug>/",
        views.DiscountDetail.as_view(),
        name="discount-update",
    ),
    path(
        "discounts/<str:slug>/",
        views.DiscountDetail.as_view(),
        name="discount-delete",
    ),
]
