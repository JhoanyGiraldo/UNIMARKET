from django.urls import path
from .views.producto_views import list_products

urlpatterns = [
    path('products/', list_products, name='api_products'),
]
