from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views
from .views.user_api_views import register_view, login_user
from .views.product_api_views import productos_api

# ------------------ Router DRF ------------------
router = routers.DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')
router.register(r'productos', views.ProductViewSet, basename='producto')
router.register(r'pedidos', views.PedidoViewSet, basename='pedido')

# ------------------ URLs ------------------
urlpatterns = [

    # ------------------ VIEWS HTML ------------------
    path('', views.index, name='index'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('carrito/', views.carrito, name='carrito'),

    # ------------------ CATÁLOGO Y FILTROS ------------------
    path("filtrar_productos/", views.filtrar_productos, name="filtrar_productos"),

    # ------------------ CARRITO ------------------
    path("carrito_count/", views.carrito_count, name="carrito_count"),
    path("agregar_carrito/", views.agregar_carrito, name="agregar_carrito"),
    path("eliminar_carrito/", views.eliminar_carrito, name="eliminar_carrito"),

    # ------------------ AUTENTICACIÓN OTP ------------------
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("otp/resend/", views.otp_resend, name="otp_resend"),

    # ------------------ PAGOS (STRIPE) ------------------
    path("crear_checkout/", views.crear_checkout, name="crear_checkout"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    # ------------------ API (JSON) ------------------
    path("api/users/register/", register_view, name="api_register"),
    path("api/users/login/", login_user, name="api_login"),
    path("api/productos/", productos_api, name="productos_api"),

    # ------------------ API carrito ------------------
    path('api/carrito/count/', views.carrito_count, name='api_carrito_count'),

    # ------------------ DRF ViewSets ------------------
    path('api/', include(router.urls)),
]

# Archivos media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
