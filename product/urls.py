"""
    Urls for product, tag, productTag models
"""
from django.urls import path
from product import views

app_name = "product"

urlpatterns = [
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
    path("top/rated", views.TopProducts.as_view(), name="top-rated"),
    path("<str:slug>", views.ProductDetail.as_view(), name="detail"),
]
