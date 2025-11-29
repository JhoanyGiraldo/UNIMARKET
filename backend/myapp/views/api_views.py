# myapp/views/api_views.py
import json, random
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password

from ..models import Usuario

@csrf_exempt
@require_POST
def api_login(request):
    try:
        data = json.loads(request.body)
        correo = data.get('correo')
        password = data.get('password')
    except:
        return JsonResponse({'success': False, 'message': 'Datos inválidos'}, status=400)

    try:
        user = Usuario.objects.get(correo=correo)
        if user.check_password(password):
            otp = str(random.randint(100000, 999999))
            request.session['otp_code'] = otp
            request.session['otp_user_id'] = user.id_usuario

            send_mail(
                'Tu código OTP',
                f'Tu código de verificación es: {otp}',
                'no-reply@tienda.com',
                [user.correo],
            )

            return JsonResponse({
                'success': True,
                'otp_required': True,
                'user': {
                    'id': user.id_usuario,
                    'correo': user.correo,
                    'nombre': user.nombre
                }
            })
        else:
            return JsonResponse({'success': False, 'message': 'Contraseña incorrecta'}, status=401)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Usuario no encontrado'}, status=401)
