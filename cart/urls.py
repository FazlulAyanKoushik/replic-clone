"""
    Urls for Cart
"""
from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('list/', views.CartList.as_view(), name='list'),
    path('item/', views.CartList.as_view(), name='item'),
]
