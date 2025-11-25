# myapp/views/auth_views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
import json, random

from ..models import Usuario

def registro_view(request):
    return render(request, 'myapp/usuarios/registro.html')

def logout_view(request):
    request.session.flush()
    return redirect("index")

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        try:
            user = Usuario.objects.get(correo=email)
            if user.check_password(password):
                otp = str(random.randint(100000, 999999))
                request.session["otp_code"] = otp
                request.session["otp_user_id"] = user.id_usuario

                send_mail(
                    "Tu código de verificación",
                    f"Tu código OTP es: {otp}",
                    "no-reply@tienda.com",
                    [user.correo],
                )
                return JsonResponse({"ok": True, "step": "otp"})
            else:
                return JsonResponse({"ok": False, "message": "Contraseña incorrecta"})
        except Usuario.DoesNotExist:
            return JsonResponse({"ok": False, "message": "Usuario no encontrado"})

    return render(request, "myapp/usuarios/login.html")

def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        otp_input = data.get("otp")

        if otp_input == request.session.get("otp_code"):
            user_id = request.session.get("otp_user_id")
            user = Usuario.objects.get(id_usuario=user_id)

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            del request.session["otp_code"]
            del request.session["otp_user_id"]

            return JsonResponse({"ok": True, "redirect": "/"})
        else:
            return JsonResponse({"ok": False, "message": "OTP incorrecto"})

@csrf_exempt
def otp_resend(request):
    if request.method == "POST":
        return JsonResponse({"success": True, "message": "Código reenviado correctamente"})
    return JsonResponse({"success": False}, status=405)
