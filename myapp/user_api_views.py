from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import json
from .models import Usuario

# ----------------------------------------
# REGISTRO DE USUARIO
# ----------------------------------------
@csrf_exempt
def register_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Datos recibidos:", data)

            nombre = data.get("nombre")
            apellido = data.get("apellido")
            # aceptar tanto "email" como "correo"
            correo = data.get("email") or data.get("correo")
            password = data.get("password")

            if not all([nombre, apellido, correo, password]):
                return JsonResponse({"ok": False, "message": "Faltan campos"}, status=400)

            if Usuario.objects.filter(correo=correo).exists():
                return JsonResponse({"ok": False, "message": "El correo ya está registrado"}, status=400)

            user = Usuario(nombre=nombre, apellido=apellido, correo=correo, rol="cliente")
            user.set_password(password)
            user.save()

            return JsonResponse({"ok": True, "message": "Usuario registrado correctamente"})
        except Exception as e:
            print("Error en register_view:", e)
            return JsonResponse({"ok": False, "message": str(e)}, status=500)

    return JsonResponse({"ok": False, "message": "Método no permitido"}, status=405)



# ----------------------------------------
# LOGIN DE USUARIO
# ----------------------------------------
@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        correo = data.get("correo")
        password = data.get("password")

        if not correo or not password:
            return JsonResponse({"success": False, "message": "Faltan credenciales"}, status=400)

        user = authenticate(username=correo, password=password)

        if user is None:
            return JsonResponse({"success": False, "message": "Credenciales incorrectas"}, status=401)

        login(request, user)

        return JsonResponse({
            "success": True,
            "message": "Login exitoso",
            "user": {
                "id": user.id_usuario,
                "nombre": user.nombre,
                "apellido": user.apellido,
                "correo": user.correo
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "JSON inválido"}, status=400)
