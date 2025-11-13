from django.urls import path, include
from rest_framework import routers
from .views import (
    BrandViewSet, CategoryViewSet, ProductViewSet, OrderViewSet,
    index, login_view, registro_view
)

# Rutas de la API
router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

# Rutas del sitio web
urlpatterns = [
    path('', index, name='index'),               # Página principal
    path('login/', login_view, name='login'),    # Página de login
    path('registro/', registro_view, name='registro'),  # Página de registro
    path('api/', include(router.urls)),          # API REST
]
