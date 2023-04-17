"""
    Urls for Category app
"""
from django.urls import path
from category import views

app_name = "category"

urlpatterns = [
    # Categories Url
    path("", views.CategoryList.as_view(), name="category-list"),
    path("detail/<str:slug>", views.CategoryDetail.as_view(), name="category-detail"),
    path(
        "products/<str:slug>",
        views.CategoryProductsBySlug.as_view(),
        name="category-products",
    ),
]
