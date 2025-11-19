import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_login_view_get(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert response.templates[0].name == "myapp/usuarios/login.html"

@pytest.mark.django_db
def test_login_view_post_valido(client):
    user = User(correo="test@test.com", nombre="Test", apellido="User")
    user.set_password("12345")
    user.save()

    response = client.post(
        reverse("login"),
        json.dumps({"email": "test@test.com", "password": "12345"}),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["step"] == "otp"
