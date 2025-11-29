from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_otp_email(correo, otp):
    send_mail(
        "Tu código de verificación",
        f"Tu código OTP es: {otp}",
        "no-reply@tiendausc.com",
        [correo],
        fail_silently=False,
    )
