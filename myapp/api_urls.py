from django.urls import path
from .views.user_api_views import register_user
from .views.producto_views import list_products

urlpatterns = [
    path('products/', list_products, name='api_products'),
    path('users/register/', register_user, name='api_register'),
]
