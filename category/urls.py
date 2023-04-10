"""
    Urls for Category app
"""
from django.urls import path
from category import views

app_name = 'category'

urlpatterns = [
    path('list/', views.CategoryList.as_view(), name='category-list'),
    path('add/', views.CategoryCreate.as_view(), name='category-add'),
    path('detail/<str:slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('update/<str:slug>/', views.CategoryUpdateDelete.as_view(), name='category-update'),
    path('delete/<str:slug>/', views.CategoryUpdateDelete.as_view(), name='category-delete'),

    path('products/<str:slug>/', views.CategoryProductsBySlug.as_view(), name='category-products'),

    # Discount urls
    path('discount/list/', views.DiscountList.as_view(), name="discount-list"),
    path('discount/add/', views.DiscountList.as_view(), name="discount-add"),
    path('discount/detail/<str:slug>/', views.DiscountDetail.as_view(), name="discount-detail"),
    path('discount/update/<str:slug>/', views.DiscountDetail.as_view(), name="discount-update"),
    path('discount/delete/<str:slug>/', views.DiscountDetail.as_view(), name="discount-delete"),
]
