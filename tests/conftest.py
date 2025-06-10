# tests/conftest.py
import sys
import os
import pytest
import app as pokebola_app

# Permite importar app.py que está na pasta-pai
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

@pytest.fixture
def client():
    # Reseta lista e contador antes de cada teste
    pokebola_app.pokemons.clear()
    pokebola_app.next_id = 1
    pokebola_app.app.testing = True

    with pokebola_app.app.test_client() as client:
        # Faz login e captura o token
        resp = client.post(
            '/login',
            json={'email': 'user@example.com', 'password': 'senha123'}
        )
        token = resp.get_json().get('access_token')
        # Adiciona o Authorization header para todas as chamadas
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        yield client
