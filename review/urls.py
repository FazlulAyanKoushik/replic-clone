"""
    Urls for category app
"""
from django.urls import path
from review import views

app_name = "review"

urlpatterns = [
    path("<str:slug>/", views.CreateProductReview.as_view(), name="add-review")
]
