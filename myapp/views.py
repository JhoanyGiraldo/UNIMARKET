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
from rest_framework import viewsets
from .models import Usuario, Producto, Categoria, Pedido, Carrito, DetalleCarrito, DireccionEnvio, Pago
from .serializers import CategoriaSerializer, ProductSerializer, PedidoSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, get_object_or_404



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
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

# ------------------ Vistas Web ------------------
def index(request):
    return render(request, 'myapp/usuarios/index.html')

def registro_view(request):
    return render(request, 'myapp/usuarios/registro.html')

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'myapp/usuarios/catalogo.html', {"productos": productos})

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

@csrf_exempt   # ⚠️ solo si usas AJAX sin CSRF, lo ideal es enviar el token
def login_view(request):
    if request.method == "POST":
        # 1. Si viene como formulario HTML
        if request.POST.get("email") and request.POST.get("password"):
            email = request.POST.get("email")
            password = request.POST.get("password")

        # 2. Si viene como JSON (AJAX)
        else:
            try:
                data = json.loads(request.body)
                email = data.get("email")
                password = data.get("password")
            except Exception:
                return JsonResponse({"ok": False, "message": "Formato inválido"}, status=400)

        # 3. Autenticación
        try:
            user = Usuario.objects.get(correo=email)
            if user.check_password(password):
                request.session['user_id'] = user.id_usuario
                request.session['user_name'] = user.nombre
                request.session['user_rol'] = user.rol

                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse({"ok": True, "redirect": "/"})
                return redirect("index")
            else:
                return JsonResponse({"ok": False, "message": "Contraseña incorrecta"}, status=401)
        except Usuario.DoesNotExist:
            return JsonResponse({"ok": False, "message": "Usuario no encontrado"}, status=404)

    return render(request, "myapp/usuarios/login.html")




def logout_view(request):
    request.session.flush()  # elimina toda la sesión
    return redirect("index")

def otp_verify_view(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('otp')
        if codigo_ingresado == request.session.get('otp_code'):
            user_id = request.session.pop('otp_user_id')
            user = Usuario.objects.get(id_usuario=user_id)
            request.session['user_id'] = user.id_usuario
            request.session['user_name'] = user.nombre
            request.session['user_rol'] = user.rol
            request.session.pop('otp_code', None)
            return redirect('index')
        else:
            messages.error(request, "Código OTP incorrecto")
    return render(request, 'myapp/usuarios/otp_verify.html')

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
    if request.method == "POST":
        data = json.loads(request.body)
        producto_id = str(data.get("producto_id"))
        cantidad = int(data.get("cantidad", 1))

        producto = get_object_or_404(Producto, id_producto=producto_id)
        carrito = request.session.get("carrito", {})

        if producto_id in carrito:
            carrito[producto_id]["cantidad"] += cantidad
        else:
            carrito[producto_id] = {
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "cantidad": cantidad
            }

        request.session["carrito"] = carrito
        return JsonResponse({"ok": True, "carrito": carrito})

@csrf_exempt
@usuario_logueado
@require_POST
def eliminar_carrito(request):
    if request.method == "POST":
        data = json.loads(request.body)
        producto_id = str(data.get("producto_id"))
        cantidad = int(data.get("cantidad", 1))

        carrito = request.session.get("carrito", {})

        if producto_id in carrito:
            carrito[producto_id]["cantidad"] -= cantidad
            if carrito[producto_id]["cantidad"] <= 0 or cantidad >= 999:
                del carrito[producto_id]

        request.session["carrito"] = carrito
        return JsonResponse({"ok": True, "carrito": carrito})

def carrito_count(request):
    # Ejemplo: contar productos en carrito de sesión
    count = request.session.get("carrito_count", 0)
    return JsonResponse({"count": count})





