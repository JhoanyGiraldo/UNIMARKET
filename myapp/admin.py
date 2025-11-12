from django.contrib import admin
from .models import Brand, Category, Product, Address, Order, OrderItem

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
