# myapp/views/utils.py
from django.http import JsonResponse

def usuario_logueado(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                "ok": False,
                "error": "Debes iniciar sesión para comprar"
            }, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper
