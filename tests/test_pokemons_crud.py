import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as c:
        # Limpa a lista global antes de cada teste
        from app import pokemons, next_id
        pokemons.clear()
        # Reinicia o contador de IDs
        # (precisa recriar a variável no módulo app)
        app.next_id = 1
        yield c

def test_create_and_list_pokemon(client):
    # 1) Cria um novo Pokémon
    response = client.post(
        '/pokemons',
        json={'name': 'Charmander'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == 'Charmander'
    assert data['captured'] is False

    # 2) Lista todos e vê se está só o Charmander
    response = client.get('/pokemons')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'Charmander'

def test_get_pokemon_by_id(client):
    # Cria dois Pokémons
    client.post('/pokemons', json={'name': 'Squirtle'})
    client.post('/pokemons', json={'name': 'Bulbasaur'})

    # GET /pokemons/2 → Bulbasaur
    response = client.get('/pokemons/2')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 2
    assert data['name'] == 'Bulbasaur'

    # GET /pokemons/99 → 404
    response = client.get('/pokemons/99')
    assert response.status_code == 404
    assert 'erro' in response.get_json()

def test_update_pokemon(client):
    # Cria um Pokémon
    client.post('/pokemons', json={'name': 'Pikachu'})

    # Atualiza o nome e o campo captured
    response = client.put(
        '/pokemons/1',
        json={'name': 'Raichu', 'captured': True}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Raichu'
    assert data['captured'] is True

    # Tenta atualizar ID inexistente → 404
    response = client.put(
        '/pokemons/99',
        json={'name': 'Mew', 'captured': False}
    )
    assert response.status_code == 404

def test_delete_pokemon(client):
    # Cria dois Pokémons
    client.post('/pokemons', json={'name': 'Eevee'})
    client.post('/pokemons', json={'name': 'Jigglypuff'})

    # Deleta o ID 1 (Eevee)
    response = client.delete('/pokemons/1')
    assert response.status_code == 204

    # Agora lista e vê se só sobrou Jigglypuff
    response = client.get('/pokemons')
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Jigglypuff'

    # Deletar ID inexistente → 404
    response = client.delete('/pokemons/99')
    assert response.status_code == 404
