from django.contrib import admin
from .models import (
    Usuario, Categoria, Producto, Carrito, DetalleCarrito,
    DireccionEnvio, Pedido, DetallePedido, Pago
)

admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(DetalleCarrito)
admin.site.register(DireccionEnvio)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Pago)
