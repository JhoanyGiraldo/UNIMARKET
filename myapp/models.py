from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ----------------------- USUARIO -----------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, contraseña=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(contraseña)  # encripta la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, contraseña=None, **extra_fields):
        extra_fields.setdefault('rol', Usuario.Rol.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, contraseña, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    class Rol(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        ADMIN = 'administrador', 'Administrador'

    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.CharField(max_length=15, choices=Rol.choices, default=Rol.CLIENTE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128, default='')


    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ----------------------- CATEGORIA -----------------------
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nombre


# ----------------------- PRODUCTO -----------------------
class Producto(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        INACTIVO = 'inactivo', 'Inactivo'

    id_producto = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)

    class Meta:
        db_table = 'producto'

    def __str__(self):
        return self.nombre


# ----------------------- DIRECCION ENVÍO -----------------------
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


# ----------------------- CARRITO -----------------------
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


# ----------------------- PEDIDO -----------------------
class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        PAGADO = 'pagado', 'Pagado'
        ENVIADO = 'enviado', 'Enviado'
        ENTREGADO = 'entregado', 'Entregado'
        CANCELADO = 'cancelado', 'Cancelado'

    id_pedido = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    direccion = models.ForeignKey(DireccionEnvio, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.PENDIENTE)

    class Meta:
        db_table = 'pedido'

    def total_pedido(self):
        return sum(d.subtotal for d in self.detalles.all())


class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_pedido'
        unique_together = ('pedido', 'producto')

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)


# ----------------------- PAGO -----------------------
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
