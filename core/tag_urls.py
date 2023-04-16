"""
    Urls for Admin users
"""
from django.urls import path
from core import views

app_name = "admin-tag"

urlpatterns = [
    # Tags urls
    path("", views.TagList.as_view(), name="tag-list"),
    path("", views.TagList.as_view(), name="tag-add"),
    path("/<str:slug>", views.TagDetail.as_view(), name="tag-detail"),
    path("/<str:slug>", views.TagDetail.as_view(), name="tag-update"),
    path("/<str:slug>", views.TagDetail.as_view(), name="tag-delete"),
]
