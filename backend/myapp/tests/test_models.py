import pytest
from myapp.models import Producto

@pytest.mark.django_db
def test_creacion_producto():
    producto = Producto.objects.create(nombre="Camisa", precio=25000)
    assert producto.nombre == "Camisa"
    assert producto.precio == 25000
