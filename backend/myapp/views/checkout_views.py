import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Configura tu clave secreta de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def crear_checkout(request):
    # Recuperar carrito desde sesión
    carrito = request.session.get("carrito", {})
    line_items = []

    for producto_id, item in carrito.items():
        line_items.append({
            "price_data": {
                "currency": "cop",  # o "cop" si quieres pesos colombianos
                "product_data": {
                    "name": item["nombre"],
                },
                "unit_amount": int(item["precio"] * 100),  # Stripe usa centavos
            },
            "quantity": item["cantidad"],
        })

    # Crear sesión de checkout en Stripe
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri("/success/"),
        cancel_url=request.build_absolute_uri("/cancel/"),
    )

    # Redirigir al checkout de Stripe
    return redirect(checkout_session.url)


def success(request):
    # Aquí puedes limpiar el carrito y registrar el pedido en tu BD
    request.session["carrito"] = {}
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")
