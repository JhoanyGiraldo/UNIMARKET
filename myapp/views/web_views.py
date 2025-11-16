# myapp/views/web_views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from ..models import Usuario, Producto
from django.contrib.auth.hashers import check_password

# ---------------------- VIEWS WEB ----------------------

def index(request):
    return render(request, 'myapp/usuarios/index.html')

def registro_view(request):
    return render(request, 'myapp/usuarios/registro.html')

def catalogo(request):
    return render(request, 'myapp/catalogo.html')

def carrito(request):
    return render(request, 'myapp/carrito.html')

def logout_view(request):
    logout(request)
    # Limpiar sesión personalizada
    request.session.flush()
    return redirect('index')

# ---------------------- LOGIN ----------------------

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('username')
        contraseña = request.POST.get('password')
        try:
            user = Usuario.objects.get(correo=correo)
            if check_password(contraseña, user.contraseña):
                request.session['user_id'] = user.id_usuario
                request.session['user_name'] = user.nombre
                request.session['user_rol'] = user.rol
                return redirect('index')  # redirige a la home
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'myapp/usuarios/login.html')

# ---------------------- PRODUCTOS (API) ----------------------

def list_products(request):
    productos = Producto.objects.all().values(
        "id_producto",
        "nombre",
        "descripcion",
        "precio",
        "stock",
        "imagen",
        "estado"
    )
    return JsonResponse(list(productos), safe=False)