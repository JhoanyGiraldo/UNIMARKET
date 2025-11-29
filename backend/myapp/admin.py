from django.contrib import admin
from .models import (
    Usuario, Categoria, Producto, Carrito, DetalleCarrito,
    DireccionEnvio, Pedido, DetallePedido, Pago
)

admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Carrito)
admin.site.register(DetalleCarrito)
admin.site.register(DireccionEnvio)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Pago)
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "stock", "estado", "categoria")
    list_filter = ("estado", "categoria")
    search_fields = ("nombre", "descripcion")

