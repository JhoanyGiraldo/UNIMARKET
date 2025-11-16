from django.shortcuts import render
from rest_framework import viewsets
from .models import Brand, Category, Product, Order
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer, OrderSerializer

# API
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Vistas del FRONT
def index(request):
    return render(request, "myapp/index.html")

def login_view(request):
    return render(request, "myapp/login.html")

def registro_view(request):
    return render(request, "myapp/registro.html")
