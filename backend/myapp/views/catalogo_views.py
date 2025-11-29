# myapp/views/catalogo_views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from ..models import Producto

def index(request):
    return render(request, 'myapp/usuarios/index.html')

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

    data = [{
        "id": p.id_producto,
        "nombre": p.nombre,
        "precio": float(p.precio),
        "stock": p.stock,
        "imagen": p.imagen.url if p.imagen else "",
    } for p in productos]

    return JsonResponse({"productos": data})

def inicio(request):
    productos = Producto.objects.filter(estado=Producto.Estado.ACTIVO)
    ofertas = Producto.objects.filter(descuento__gt=0)

    usuario = request.user if request.user.is_authenticated else None

    return render(request, "inicio.html", {
        "productos": productos,
        "ofertas": ofertas,
        "usuario": usuario
    })
