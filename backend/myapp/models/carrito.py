from django.db import models
from .usuario import Usuario
from .producto import Producto


class Carrito(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        COMPLETADO = 'completado', 'Completado'

    id_carrito = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carritos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.ACTIVO)

    class Meta:
        db_table = 'carrito'

    def agregar_producto(self, producto, cantidad=1):
        detalle, created = DetalleCarrito.objects.get_or_create(
            carrito=self,
            producto=producto,
            defaults={
                'cantidad': cantidad,
                'precio_unitario': producto.precio,
                'subtotal': producto.precio * cantidad
            }
        )
        if not created:
            detalle.cantidad += cantidad
            detalle.subtotal = detalle.cantidad * detalle.precio_unitario
            detalle.save()
        return detalle

    def eliminar_producto(self, producto, cantidad=1):
        try:
            detalle = DetalleCarrito.objects.get(carrito=self, producto=producto)
            detalle.cantidad -= cantidad
            if detalle.cantidad <= 0:
                detalle.delete()
            else:
                detalle.subtotal = detalle.cantidad * detalle.precio_unitario
                detalle.save()
            return True
        except DetalleCarrito.DoesNotExist:
            return False

    def total_carrito(self):
        return sum(d.subtotal for d in self.detalles.all())


class DetalleCarrito(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_carrito'
        unique_together = ('carrito', 'producto')

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
