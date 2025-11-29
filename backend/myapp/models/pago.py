from django.db import models
from .pedido import Pedido


class Pago(models.Model):
    class Metodo(models.TextChoices):
        STRIPE = 'stripe', 'Stripe'
        EFECTIVO = 'efectivo', 'Efectivo'
        TRANSFERENCIA = 'transferencia', 'Transferencia'
        PSE = 'pse', 'PSE'

    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        EXITOSO = 'exitoso', 'Exitoso'
        FALLIDO = 'fallido', 'Fallido'

    id_pago = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pagos')
    metodo = models.CharField(max_length=20, choices=Metodo.choices)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.PENDIENTE)
    stripe_payment_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'pago'
