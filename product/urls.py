"""
    Urls for product, tag, productTag models
"""
from django.urls import path
from product import views

app_name = "product"

urlpatterns = [
    # Tags urls
    path("tags", views.TagList.as_view(), name="tag-list"),
    path("tags", views.TagList.as_view(), name="tag-add"),
    path("tags/<str:slug>", views.TagDetail.as_view(), name="tag-detail"),
    path("tags/<str:slug>", views.TagDetail.as_view(), name="tag-update"),
    path("tags/<str:slug>", views.TagDetail.as_view(), name="tag-delete"),
    # TagConnector urls
    path("tag/connectors", views.TagConnectorList.as_view(), name="connector-list"),
    path("tag/connectors", views.TagConnectorList.as_view(), name="connector-add"),
    path(
        "tag/connectors/<str:pk>",
        views.TagConnectorDetail.as_view(),
        name="connector-detail",
    ),
    path(
        "tag/connectors/<str:pk>",
        views.TagConnectorDetail.as_view(),
        name="connector-update",
    ),
    path(
        "tag/connectors/<str:pk>",
        views.TagConnectorDetail.as_view(),
        name="connector-delete",
    ),
    # Products urls
    path("", views.ProductList.as_view(), name="list"),
    path("add", views.ProductCreate.as_view(), name="create"),
    path("top/rated", views.TopProducts.as_view(), name="top-rated"),
    path("<str:slug>", views.ProductDetail.as_view(), name="detail"),
    path("<str:slug>/", views.ProductUpdateDelete.as_view(), name="update"),
    path("<str:slug>/", views.ProductUpdateDelete.as_view(), name="delete"),
]
