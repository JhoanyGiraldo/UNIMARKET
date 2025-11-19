def user_context(request):
    return {
        "user_id": request.session.get("user_id"),
        "user_name": request.session.get("user_name"),
        "user_rol": request.session.get("user_rol"),
    }
def carrito(request):
    return {
        "carrito": request.session.get("carrito", [])
    }
