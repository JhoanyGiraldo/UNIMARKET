import pytest
from django.urls import reverse, resolve
from myapp.views import catalogo

def test_url_catalogo_resuelve():
    url = reverse('catalogo')
    match = resolve(url)
    assert match.func == catalogo
