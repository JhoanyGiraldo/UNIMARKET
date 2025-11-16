# myapp/views/web_views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets
from .models import Usuario, Producto, Brand, Category, Order
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer, OrderSerializer

# ---------------------- VIEWS WEB ----------------------

def index(request):
    # Si quieres mostrar el nombre del usuario logueado
    user_name = request.session.get('user_name')
    return render(request, 'myapp/index.html', {"user_name": user_name})

def registro_view(request):
    return render(request, 'myapp/usuarios/registro.html')

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'myapp/catalogo.html', {"productos": productos})

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
                # Guardar datos del usuario en sesión
                request.session['user_id'] = user.id_usuario
                request.session['user_name'] = user.nombre
                request.session['user_rol'] = user.rol
                return redirect('index')  # Redirige a home
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

# ---------------------- API (DRF ViewSets) ----------------------

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
