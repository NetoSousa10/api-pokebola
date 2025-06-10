# flake8: noqa E402, E302

import sys
import os

# 1) Insere a pasta-pai (onde está app.py) no início do PYTHONPATH
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

import pytest
import app as pokebola_app  # agora o Python encontra app.py corretamente


@pytest.fixture
def client():
    pokebola_app.pokemons.clear()
    pokebola_app.next_id = 1
    pokebola_app.app.testing = True

    with pokebola_app.app.test_client() as client:
        # login automático para obter o JWT
        resp = client.post(
            '/login',
            json={'email': 'user@example.com', 'password': 'senha123'}
        )
        token = resp.get_json().get('access_token')
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        yield client
