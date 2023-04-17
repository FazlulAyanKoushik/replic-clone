"""
    Urls for Admin users
"""
from django.urls import path
from core import views

app_name = "admin-product"

urlpatterns = [
    # Product urls
    path("", views.ProductCreate.as_view(), name="create"),
    path("/<str:slug>/", views.ProductUpdateDelete.as_view(), name="update"),
    path("/<str:slug>/", views.ProductUpdateDelete.as_view(), name="delete"),
    path("/<str:slug>/", views.ProductUpdateDelete.as_view(), name="partial-update"),
]
