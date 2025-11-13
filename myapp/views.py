from django.shortcuts import render
from rest_framework import viewsets
from .models import Brand, Category, Product, Order
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer, OrderSerializer

# Vistas API
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

# Vistas HTML
def index(request):
    return render(request, 'usuarios/index.html')

def login_view(request):
    return render(request, 'usuarios/login.html')

def registro_view(request):
    return render(request, 'usuarios/registro.html')
