from .home_views import index
from .carrito_views import  carrito, agregar_carrito, eliminar_carrito, carrito_count
from .catalogo_views import catalogo, filtrar_productos
from .auth_views import login_view, logout_view, registro_view, verify_otp, otp_resend
from .pedido_views import crear_checkout
from .viewsets import CategoriaViewSet, ProductViewSet, PedidoViewSet
