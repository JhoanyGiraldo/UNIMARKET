from django.urls import path
from .user_api_views import register_user, login_user

urlpatterns = [
    path('users/register/', register_user, name='api_register'),
    path('users/login/', login_user, name='login_user'),
]