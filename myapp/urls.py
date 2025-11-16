from django.urls import path
from .views.web_views import index, login_view, registro_view, logout_view

urlpatterns = [
    path("", index, name="index"),
    path("login/", login_view, name="login"),
    path("registro/", registro_view, name="registro"),
    path("logout/", logout_view, name="logout"),
]
