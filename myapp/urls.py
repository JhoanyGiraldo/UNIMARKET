from django.urls import path, include
from rest_framework import routers
from .user_api_views import register_view, login_user
from .product_api_views import productos_api
from . import  views
from django.conf import settings
from django.conf.urls.static import static

# ------------------ Router DRF para API REST ------------------
router = routers.DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')
router.register(r'productos', views.ProductViewSet, basename='producto')
router.register(r'pedidos', views.PedidoViewSet, basename='pedido')

# ------------------ URLs de la aplicación ------------------
urlpatterns = [
    # Vistas Web (HTML)
    path('', views.index, name='index'),
    path('registro/', views.registro_view, name='registro'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('carrito/', views.carrito, name='carrito'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("carrito_count/", views.carrito_count, name="carrito_count"),
    path("agregar_carrito/", views.agregar_carrito, name="agregar_carrito"),
    path("eliminar_carrito/", views.eliminar_carrito, name="eliminar_carrito"),
    path("filtrar_productos/", views.filtrar_productos, name="filtrar_productos"),
    
    # API para login
    path("api/users/register/", register_view, name="api_register"),
    path("api/users/login/", login_user, name="api_login"),
    path("productos_api/", productos_api, name="productos_api"),

    # API carrito
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path('api/carrito/count/', views.carrito_count, name='api_carrito_count'),

    # DRF ViewSets
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
