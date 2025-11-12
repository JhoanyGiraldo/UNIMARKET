from django.urls import path, include
from rest_framework import routers
from .views import BrandViewSet, CategoryViewSet, ProductViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
