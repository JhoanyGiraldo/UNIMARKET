from django.http import JsonResponse
from ..models import Producto

def productos_api(request):
    productos = Producto.objects.filter(estado=Producto.Estado.ACTIVO).values(
        "id_producto",
        "nombre",
        "descripcion",
        "precio",
        "stock",
        "imagen",
        "estado",
        "categoria__nombre"   # 👈 accede al nombre de la categoría relacionada
    )
    return JsonResponse({"productos": list(productos)})
