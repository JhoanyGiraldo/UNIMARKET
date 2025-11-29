import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_contexto_global(client):
    response = client.get(reverse('index'))
    assert 'carrito' in response.context
