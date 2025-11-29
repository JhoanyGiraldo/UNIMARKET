# myapp/views/carrito_views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from ..models import Producto
from .utils import usuario_logueado

def _carrito_detallado(carrito):
    detallado = {}
    for pid, item in carrito.items():
        producto = Producto.objects.filter(id_producto=pid).first()
        if producto:
            detallado[pid] = {
                "nombre": producto.nombre,
                "descripcion": getattr(producto, "descripcion", ""),
                "precio": float(producto.precio),
                "cantidad": item["cantidad"],
            }
    return detallado
def carrito(request):
    carrito = request.session.get("carrito", {})
    items = []  # <- inicializamos la lista

    for pid, item in carrito.items():
        producto = Producto.objects.filter(id_producto=pid).first()
        if producto:
            subtotal = item["cantidad"] * item["precio"]
            items.append({
                "producto": producto,
                "precio_unitario": item["precio"],
                "cantidad": item["cantidad"],
                "subtotal": subtotal
            })

    return render(request, "myapp/usuarios/carrito.html", {
        "items": items,          # <- ahora sí existe
        "carrito": carrito       # <- para el JS
    })


@csrf_exempt
@usuario_logueado
@require_POST
def agregar_carrito(request):
    data = json.loads(request.body)
    producto_id = str(data.get("producto_id"))
    cantidad = int(data.get("cantidad", 1))

    producto = Producto.objects.filter(id_producto=producto_id).first()
    if not producto:
        return JsonResponse({"ok": False, "error": "Producto no encontrado"})

    carrito = request.session.get("carrito", {})
    cantidad_actual = carrito.get(producto_id, {}).get("cantidad", 0)
    nueva_cantidad = cantidad_actual + cantidad

    if nueva_cantidad > producto.stock:
        return JsonResponse({"ok": False, "error": "Stock insuficiente"})

    carrito[producto_id] = {
        "nombre": producto.nombre,
        "precio": float(producto.precio),
        "cantidad": nueva_cantidad,
        "precio_unitario": float(producto.precio)
    }

    request.session["carrito"] = carrito
    return JsonResponse({"ok": True, "carrito": carrito})

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

    print("Carrito actualizado:", request.session["carrito"])
    request.session["carrito"] = carrito
    return JsonResponse({"ok": True, "carrito": carrito})

def carrito_count(request):
    carrito = request.session.get("carrito", {})
    count = sum(item["cantidad"] for item in carrito.values())
    return JsonResponse({"count": count})

def carrito_total(request):
    carrito = request.session.get("carrito", {})
    total = sum(item["precio_unitario"] * item["cantidad"] for item in carrito.values())
    return JsonResponse({"total": total})

