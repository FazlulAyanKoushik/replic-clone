"""
    Urls for product, tag, productTag models
"""
from django.urls import path
from product import views

app_name = 'product'

urlpatterns = [
    # Product urls
    path('list/', views.ProductList.as_view(), name='list'),
    path('create/', views.ProductCreate.as_view(), name='create'),
    path('top/rated/', views.TopProducts.as_view(), name='top-rated'),
    path('detail/<str:slug>/', views.ProductDetail.as_view(), name='detail'),
    path('update/<str:slug>/', views.ProductUpdateDelete.as_view(), name='update'),
    path('delete/<str:slug>/', views.ProductUpdateDelete.as_view(), name='delete'),

    # Tags urls
    path('tag/list/', views.TagList.as_view(), name='tag-list'),
    path('tag/add/', views.TagList.as_view(), name='tag-add'),
    path('tag/detail/<str:slug>/', views.TagDetail.as_view(), name='tag-detail'),
    path('tag/update/<str:slug>/', views.TagDetail.as_view(), name='tag-update'),
    path('tag/delete/<str:slug>/', views.TagDetail.as_view(), name='tag-delete'),

    # ProductTagConnector urls
    path('connector/list/', views.TagConnectorList.as_view(), name='connector-list'),
    path('connector/add/', views.TagConnectorList.as_view(), name='connector-add'),
    path('connector/detail/<str:pk>/', views.TagConnectorDetail.as_view(), name='connector-detail'),
    path('connector/update/<str:pk>/', views.TagConnectorDetail.as_view(), name='connector-update'),
    path('connector/delete/<str:pk>/', views.TagConnectorDetail.as_view(), name='connector-delete'),
]
