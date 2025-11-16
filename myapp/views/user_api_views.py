from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        correo = data.get("correo")
        password = data.get("password")

        if not all([nombre, apellido, correo, password]):
            return JsonResponse({"error": "Faltan datos"}, status=400)

        if User.objects.filter(username=correo).exists():
            return JsonResponse({"error": "Usuario ya existe"}, status=400)

        user = User.objects.create_user(
            username=correo,
            email=correo,
            first_name=nombre,
            last_name=apellido,
            password=password
        )
        return JsonResponse({"success": True, "user_id": user.id})
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
