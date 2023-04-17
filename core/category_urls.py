"""
    Urls for Admin users
"""
from django.urls import path
from core import views

app_name = "admin-category"

urlpatterns = [
    path("", views.CategoryCreate.as_view(), name="category-add"),
    path(
        "<str:slug>",
        views.CategoryUpdateDelete.as_view(),
        name="category-update",
    ),
    path(
        "<str:slug>",
        views.CategoryUpdateDelete.as_view(),
        name="category-delete",
    ),
]
