from django.db import models



# ----------------------- USUARIO -----------------------
class Usuario(models.Model):
    class Rol(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        ADMIN = 'administrador', 'Administrador'

    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150, unique=True)
    contraseña = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rol = models.CharField(max_length=15, choices=Rol.choices, default=Rol.CLIENTE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=255, null=True, blank=True)
    two_factor_verified = models.BooleanField(default=False)

    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'usuario'


# ----------------------- CATEGORIA -----------------------
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'categoria'


# ----------------------- PRODUCTO -----------------------
class Producto(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        INACTIVO = 'inactivo', 'Inactivo'

    id_producto = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)

    class Meta:
        db_table = 'producto'


# ----------------------- DIRECCION ENVÍO -----------------------
class DireccionEnvio(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'direccion_envio'


# ----------------------- CARRITO -----------------------
class Carrito(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        COMPLETADO = 'completado', 'Completado'

    id_carrito = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.ACTIVO)

    class Meta:
        db_table = 'carrito'


# ----------------------- DETALLE CARRITO -----------------------
class DetalleCarrito(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_carrito'


# ----------------------- PEDIDO -----------------------
class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        PAGADO = 'pagado', 'Pagado'
        ENVIADO = 'enviado', 'Enviado'
        ENTREGADO = 'entregado', 'Entregado'
        CANCELADO = 'cancelado', 'Cancelado'

    id_pedido = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    direccion = models.ForeignKey(DireccionEnvio, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.PENDIENTE)

    class Meta:
        db_table = 'pedido'


# ----------------------- DETALLE PEDIDO -----------------------
class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_pedido'


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
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    metodo = models.CharField(max_length=20, choices=Metodo.choices)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=Estado.choices, default=Estado.PENDIENTE)
    stripe_payment_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'pago'