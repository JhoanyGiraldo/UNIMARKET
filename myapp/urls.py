from django.urls import path
from myapp.views.web_views import index, login_view, registro_view, catalogo, carrito, logout_view

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro_view, name='registro'),
    path('catalogo/', catalogo, name='catalogo'),
    path('carrito/', carrito, name='carrito'),
]
