from django.urls import path, include
from rest_framework import routers
from .views import (
    BrandViewSet, CategoryViewSet, ProductViewSet, OrderViewSet,
    index, login_view, registro_view
)

router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('api/', include(router.urls)),
]
