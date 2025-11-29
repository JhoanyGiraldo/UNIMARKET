import pytest
from myapp.models import Producto

@pytest.mark.django_db
def test_api_get_productos(client):
    Producto.objects.create(nombre="Zapatos", precio=80000)
    response = client.get('/api/productos/')
    assert response.status_code == 200
    assert "Zapatos" in response.content.decode()
