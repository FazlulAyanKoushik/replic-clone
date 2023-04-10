"""
    Urls for user app
"""
from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'user'

urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('detail/', views.UserDetailUpdate.as_view(), name='detail'),
    path('update/', views.UserDetailUpdate.as_view(), name='update'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    # Token urls
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Admin urls
    path('all/', views.GetAllUsers.as_view(), name='get-users'),
    path('delete/<str:pk>/', views.DeleteUser.as_view(), name='delete-user'),
]
