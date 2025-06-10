
def test_capture_changes_state(client):
    # Cria um Pokémon (criado com JWT)
    resp = client.post('/pokemons', json={'name': 'Charmander'})
    assert resp.status_code == 201

    resultados = set()
    for _ in range(5):
        response = client.get('/capture/1')
        assert response.status_code == 200
        data = response.get_json()
        assert 'captured' in data
        resultados.add(data['captured'])

    # Deve ter aparecido True e False
    assert True in resultados
    assert False in resultados


def test_capture_invalid_id(client):
    response = client.get('/capture/999')
    assert response.status_code == 404
