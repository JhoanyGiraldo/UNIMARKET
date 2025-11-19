from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
import random
import json
from django import forms
from rest_framework import viewsets
from .models import Usuario, Producto, Categoria, Pedido, Carrito, DetalleCarrito, DireccionEnvio, Pago
from .serializers import CategoriaSerializer, ProductSerializer, PedidoSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login
import stripe
from django.conf import settings
# ------------------ DRF ViewSets ------------------
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
# ------------------ Decorador para validar sesión ------------------
def usuario_logueado(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"ok": False, "error": "Debes iniciar sesión para comprar"}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


# ------------------ Vistas Web ------------------
def index(request):
    return render(request, 'myapp/usuarios/index.html')

def registro_view(request):
    return render(request, 'myapp/usuarios/registro.html')

def catalogo(request):
    query = request.GET.get("q", "")
    categoria = request.GET.get("categoria", "")

    productos = Producto.objects.all()

    if query:
        productos = productos.filter(nombre__icontains=query)

    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    return render(request, "myapp/usuarios/catalogo.html", {
        "productos": productos,
        "query": query,
        "categoria": categoria,
    })

def filtrar_productos(request):
    query = request.GET.get("q", "")
    categoria = request.GET.get("categoria", "")

    productos = Producto.objects.all()

    if query:
        productos = productos.filter(nombre__icontains=query)

    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    data = []
    for p in productos:
        data.append({
            "id": p.id_producto,
            "nombre": p.nombre,
            "precio": float(p.precio),
            "stock": p.stock,
            "imagen": p.imagen.url if p.imagen else "",
        })

    return JsonResponse({"productos": data})

def carrito(request):
    carrito = request.session.get("carrito", {})
    items = []
    total = 0

    for producto_id, datos in carrito.items():
        producto = get_object_or_404(Producto, id_producto=producto_id)
        cantidad = datos["cantidad"]
        precio_unitario = datos["precio"]
        subtotal = cantidad * precio_unitario
        total += subtotal

        items.append({
            "producto": producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal
        })

    return render(request, "myapp/usuarios/carrito.html", {"items": items, "total": total})

def inicio(request):
    # Productos activos
    productos = Producto.objects.filter(estado=Producto.Estado.ACTIVO)

    # Ofertas: por ejemplo, productos con descuento > 0
    ofertas = Producto.objects.filter(descuento__gt=0)

    usuario = request.user if request.user.is_authenticated else None

    return render(request, "inicio.html", {
        "productos": productos,
        "ofertas": ofertas,
        "usuario":  usuario
    })

@csrf_exempt   # ⚠️ solo si usas AJAX sin CSRF, lo ideal es enviar el token

def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        try:
            user = Usuario.objects.get(correo=email)
            if user.check_password(password):
                # Generar OTP
                otp = str(random.randint(100000, 999999))
                request.session["otp_code"] = otp
                request.session["otp_user_id"] = user.id_usuario

                # Enviar OTP al correo
                send_mail(
                    "Tu código de verificación",
                    f"Tu código OTP es: {otp}",
                    "no-reply@tiendausc.com",
                    [user.correo],
                    fail_silently=False,
                )
                return JsonResponse({"ok": True, "step": "otp"})
            else:
                return JsonResponse({"ok": False, "message": "Contraseña incorrecta"})
        except Usuario.DoesNotExist:
            return JsonResponse({"ok": False, "message": "Usuario no encontrado"})


    return render(request, "myapp/usuarios/login.html", {"form": forms})




def logout_view(request):
    request.session.flush()  # elimina toda la sesión
    return redirect("index")

import json
from django.http import JsonResponse
from .models import Usuario

from django.http import JsonResponse
from .models import Usuario
import json



def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        otp_input = data.get("otp")

        if otp_input == request.session.get("otp_code"):
            user_id = request.session.get("otp_user_id")
            user = Usuario.objects.get(id_usuario=user_id)

            # ✅ Aquí conectas con el sistema de autenticación
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # Opcional: mantener tus datos personalizados
            request.session["user_id"] = user.id_usuario
            request.session["user_name"] = user.nombre
            request.session["user_rol"] = user.rol

            del request.session["otp_code"]
            del request.session["otp_user_id"]

            return JsonResponse({"ok": True, "redirect": "/"})
        else:
            return JsonResponse({"ok": False, "message": "Código OTP inválido"})

@csrf_exempt
def otp_resend(request):
    if request.method == "POST":
        data = json.loads(request.body)
        correo = data.get("correo")
        
        return JsonResponse({"success": True, "message": "Código reenviado correctamente"})

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)




# ------------------ API ------------------
@csrf_exempt
@require_POST
def api_login(request):
    try:
        data = json.loads(request.body)
        correo = data.get('correo')
        password = data.get('password')
    except Exception:
        return JsonResponse({'success': False, 'message': 'Datos inválidos'}, status=400)

    if not correo or not password:
        return JsonResponse({'success': False, 'message': 'Faltan datos'}, status=400)

    try:
        user = Usuario.objects.get(correo=correo)
        if check_password(password, user.contraseña):
            otp = str(random.randint(100000, 999999))
            request.session['otp_code'] = otp
            request.session['otp_user_id'] = user.id_usuario

            send_mail(
                'Tu código OTP',
                f'Tu código de verificación es: {otp}',
                'no-reply@tiendausc.com',
                [user.correo],
                fail_silently=False,
            )

            return JsonResponse({
                'success': True,
                'otp_required': True,
                'user': {
                    'id': user.id_usuario,
                    'correo': user.correo,
                    'nombre': user.nombre
                }
            })
        else:
            return JsonResponse({'success': False, 'message': 'Usuario o contraseña incorrectos'}, status=401)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Usuario o contraseña incorrectos'}, status=401)

@csrf_exempt
@usuario_logueado
@require_POST
def agregar_carrito(request):
    data = json.loads(request.body)
    producto_id = str(data.get("producto_id"))
    cantidad = int(data.get("cantidad", 1))

    producto = Producto.objects.filter(id_producto=producto_id).first()
    if not producto:
        return JsonResponse({ "ok": False, "error": "Producto no encontrado" })

    carrito = request.session.get("carrito", {})

    cantidad_actual = carrito.get(producto_id, {}).get("cantidad", 0)
    nueva_cantidad = cantidad_actual + cantidad

    if nueva_cantidad > producto.stock:
        return JsonResponse({ "ok": False, "error": "Stock insuficiente" })

    carrito[producto_id] = {
        "nombre": producto.nombre,
        "precio": float(producto.precio),   # 🔥 convertir Decimal a float
        "cantidad": nueva_cantidad,
        "precio_unitario": float(producto.precio),  # 🔥 también aquí
    }

    request.session["carrito"] = carrito
    request.session.modified = True
    return JsonResponse({ "ok": True, "carrito": carrito })

@csrf_exempt
@usuario_logueado
@require_POST
def eliminar_carrito(request):
    data = json.loads(request.body)
    producto_id = str(data.get("producto_id"))
    cantidad = int(data.get("cantidad", 1))

    carrito = request.session.get("carrito", {})

    if producto_id == "all":
        carrito = {}
    elif producto_id in carrito:
        carrito[producto_id]["cantidad"] -= cantidad
        if carrito[producto_id]["cantidad"] <= 0:
            del carrito[producto_id]

    request.session["carrito"] = carrito
    request.session.modified = True
    return JsonResponse({ "ok": True, "carrito": carrito })


def carrito_count(request):
    # Ejemplo: contar productos en carrito de sesión
    count = request.session.get("carrito_count", 0)
    return JsonResponse({"count": count})

stripe.api_key = settings.STRIPE_SECRET_KEY

def crear_checkout(request):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "cop",
                "product_data": {
                    "name": "Bolígrafo USC",
                },
                "unit_amount": 15000 * 100,  # en centavos
            },
            "quantity": 2,
        }],
        mode="payment",
        success_url="https://tuapp.com/success",
        cancel_url="https://tuapp.com/cancel",
    )
    return redirect(session.url)




