# myapp/views/pedido_views.py
import stripe
from django.conf import settings
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY

def crear_checkout(request):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "cop",
                "product_data": {
                    "name": "Bolígrafo USC",
                },
                "unit_amount": 15000 * 100,
            },
            "quantity": 2,
        }],
        mode="payment",
        success_url="https://tuapp.com/success",
        cancel_url="https://tuapp.com/cancel",
    )
    return redirect(session.url)
