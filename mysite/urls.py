from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # 👈 incluye todas las rutas de myapp
    path('api/', include('myapp.api_urls')),  # rutas de API
]
