# tests/conftest.py

import sys
import os

# 1) Insere a pasta-pai (onde está app.py) no início do PYTHONPATH
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

import pytest
import app as pokebola_app  # só agora importamos o app, com o path correto

@pytest.fixture
def client():
    # Reseta lista e contador antes de cada teste
    pokebola_app.pokemons.clear()
    pokebola_app.next_id = 1
    pokebola_app.app.testing = True

    with pokebola_app.app.test_client() as client:
        # Faz login automático para JWT
        resp = client.post(
            '/login',
            json={'email': 'user@example.com', 'password': 'senha123'}
        )
        token = resp.get_json().get('access_token')
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        yield client
