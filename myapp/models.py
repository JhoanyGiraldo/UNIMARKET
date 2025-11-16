from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# ============================
#          BRAND (marca)
# ============================
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'marca'

    def __str__(self):
        return self.name


# ============================
#        CATEGORY (categoria)
# ============================
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'categoria'
        managed = False

    def __str__(self):
        return self.nombre



# ============================
#         PRODUCT (producto)
# ============================
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey('Categoria', db_column='id_categoria', on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=[('activo', 'activo'), ('inactivo', 'inactivo')], default='activo')

    class Meta:
        db_table = 'producto'
        managed = False

    def __str__(self):
        return self.nombre
    
class DireccionEnvio(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', db_column='id_usuario', on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'direccion_envio'
        managed = False

    def __str__(self):
        return f"{self.direccion}, {self.ciudad}"

# ============================
#          ORDER (pedido)
# ============================
class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PAID', 'Paid'),
        ('SHIPPED', 'Shipped'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(DireccionEnvio, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_reference = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'pedido'

    def __str__(self):
        return f"Order #{self.id} - {self.user}"


# ============================
#       ORDER ITEM (detalle_pedido)
# ============================
class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey('Pedido', db_column='id_pedido', on_delete=models.CASCADE)
    id_producto = models.ForeignKey('Producto', db_column='id_producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'detalle_pedido'
        managed = False

    
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=150, unique=True)
    contraseña = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=[('cliente', 'cliente'), ('administrador', 'administrador')], default='cliente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=255, null=True, blank=True)
    two_factor_verified = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'usuario'
        managed = False

    def __str__(self):
        return self.correo
    

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', db_column='id_usuario', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('activo', 'activo'), ('completado', 'completado')], default='activo')

    class Meta:
        db_table = 'carrito'
        managed = False

class DetalleCarrito(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_carrito = models.ForeignKey('Carrito', db_column='id_carrito', on_delete=models.CASCADE)
    id_producto = models.ForeignKey('Producto', db_column='id_producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_carrito'
        managed = False

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', db_column='id_usuario', on_delete=models.CASCADE)
    id_direccion = models.ForeignKey('DireccionEnvio', db_column='id_direccion', on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'pendiente'),
        ('pagado', 'pagado'),
        ('enviado', 'enviado'),
        ('entregado', 'entregado')
    ], default='pendiente')

    class Meta:
        db_table = 'pedido'
        managed = False



class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey('Pedido', db_column='id_pedido', on_delete=models.CASCADE)
    metodo = models.CharField(max_length=20, choices=[
        ('stripe', 'stripe'),
        ('efectivo', 'efectivo'),
        ('transferencia', 'transferencia'),
        ('pse', 'pse'),
    ])
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'pendiente'),
        ('exitoso', 'exitoso'),
        ('fallido', 'fallido'),
    ], default='pendiente')
    stripe_payment_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'pago'
        managed = False


