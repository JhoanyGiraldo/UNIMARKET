from django.db import models
from .usuario import Usuario


class DireccionEnvio(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='direcciones')
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'direccion_envio'

    def __str__(self):
        return f"{self.direccion}, {self.ciudad}"
