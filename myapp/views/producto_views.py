from django.http import JsonResponse
from ..models import Producto

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
