from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'myapp/usuarios/index.html')

def login_view(request):
    return render(request, 'myapp/usuarios/login.html')

def registro_view(request):
    return render(request, 'myapp/usuarios/registro.html')

def logout_view(request):
    logout(request)
    return redirect('index')
