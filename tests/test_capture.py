import pytest
import app as pokebola_app
from app import app


@pytest.fixture
def client():
    pokebola_app.pokemons.clear()
    pokebola_app.next_id = 1
    pokebola_app.app.testing = True
    with pokebola_app.app.test_client() as client:
        yield client


def test_capture_changes_state(client):
    client.post('/pokemons', json={'name': 'Charmander'})

    resultados = set()
    for _ in range(5):
        response = client.get('/capture/1')
        assert response.status_code == 200
        data = response.get_json()
        assert 'captured' in data
        resultados.add(data['captured'])

    assert True in resultados
    assert False in resultados

    response = client.get('/capture/99')
    assert response.status_code == 404
