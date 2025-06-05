import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as c:
        # Zera a lista e o contador antes de cada teste
        from app import pokemons, next_id
        pokemons.clear()
        app.next_id = 1
        yield c

def test_capture_changes_state(client):
    # Cria um Pokémon nome “Charmander”
    client.post('/pokemons', json={'name': 'Charmander'})

    # Ao chamar /capture/1 várias vezes, ele deve retornar 200 e alterar captured
    resultados = set()
    for _ in range(5):
        response = client.get('/capture/1')
        assert response.status_code == 200
        data = response.get_json()
        assert 'captured' in data
        resultados.add(data['captured'])

    # Ao menos True e False devem aparecer em algum momento (chance aleatória)
    assert True in resultados
    assert False in resultados

    # Se tentar capturar ID inexistente → 404
    response = client.get('/capture/99')
    assert response.status_code == 404
