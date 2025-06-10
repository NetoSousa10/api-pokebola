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


def test_create_and_list_pokemon(client):
    response = client.post("/pokemons", json={"name": "Charmander"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Charmander"
    assert data["captured"] is False

    response = client.get("/pokemons")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Charmander"


def test_get_pokemon_by_id(client):
    client.post("/pokemons", json={"name": "Squirtle"})
    client.post("/pokemons", json={"name": "Bulbasaur"})

    response = client.get("/pokemons/2")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 2
    assert data["name"] == "Bulbasaur"

    response = client.get("/pokemons/99")
    assert response.status_code == 404
    assert "erro" in response.get_json()


def test_update_pokemon(client):
    client.post("/pokemons", json={"name": "Pikachu"})

    response = client.put("/pokemons/1", json={"name": "Raichu", "captured": True})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Raichu"
    assert data["captured"] is True

    response = client.put("/pokemons/99", json={"name": "Mew", "captured": False})
    assert response.status_code == 404


def test_delete_pokemon(client):
    client.post("/pokemons", json={"name": "Eevee"})
    client.post("/pokemons", json={"name": "Jigglypuff"})

    response = client.delete("/pokemons/1")
    assert response.status_code == 204

    response = client.get("/pokemons")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Jigglypuff"

    response = client.delete("/pokemons/99")
    assert response.status_code == 404
