from flask import Flask, jsonify, request, redirect, url_for
from flasgger import Swagger, swag_from
import random


app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'API de Pokébola',
    'uiversion': 3,
    'definitions': {
        'Pokemon': {
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'integer',
                    'example': 1
                },
                'name': {
                    'type': 'string',
                    'example': 'Pikachu'
                },
                'captured': {
                    'type': 'boolean',
                    'example': False
                }
            },
            'required': ['id', 'name', 'captured']
        },
        'PokemonInput': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    'example': 'Charmander'
                }
            },
            'required': ['name']
        }
    }
}
Swagger(app)


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('flasgger.apidocs'))


pokemons = []
next_id = 1


@app.route('/pokemons', methods=['GET'])
@swag_from({
    'tags': ['Pokemons'],
    'responses': {
        200: {
            'description': 'Lista todos os pokemons',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Pokemon'
                }
            }
        }
    }
})
def list_pokemons():
    return jsonify(pokemons), 200


@app.route('/pokemons/<int:pokemon_id>', methods=['GET'])
@swag_from({
    'tags': ['Pokemons'],
    'parameters': [
        {
            'name': 'pokemon_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do pokemon'
        }
    ],
    'responses': {
        200: {
            'description': 'Retorna um pokemon pelo ID',
            'schema': {
                '$ref': '#/definitions/Pokemon'
            }
        },
        404: {
            'description': 'Pokemon não encontrado'
        }
    }
})
def get_pokemon(pokemon_id):
    for p in pokemons:
        if p['id'] == pokemon_id:
            return jsonify(p), 200
    return jsonify({'erro': 'Pokémon não encontrado'}), 404


@app.route('/pokemons', methods=['POST'])
@swag_from({
    'tags': ['Pokemons'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                '$ref': '#/definitions/PokemonInput'
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Pokemon criado com sucesso',
            'schema': {
                '$ref': '#/definitions/Pokemon'
            }
        },
        400: {
            'description': 'Campo name é obrigatório'
        }
    }
})
def create_pokemon():
    global next_id
    dados = request.get_json()
    if not dados or 'name' not in dados:
        return jsonify({'erro': 'Campo name é obrigatório'}), 400

    novo = {
        'id': next_id,
        'name': dados['name'],
        'captured': False
    }
    pokemons.append(novo)
    next_id += 1
    return jsonify(novo), 201


@app.route('/pokemons/<int:pokemon_id>', methods=['PUT'])
@swag_from({
    'tags': ['Pokemons'],
    'parameters': [
        {
            'name': 'pokemon_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do pokemon'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'Charmander'
                    },
                    'captured': {
                        'type': 'boolean',
                        'example': False
                    }
                },
                'required': ['name', 'captured']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Pokemon atualizado com sucesso',
            'schema': {
                '$ref': '#/definitions/Pokemon'
            }
        },
        400: {
            'description': 'Campos name e captured obrigatórios'
        },
        404: {
            'description': 'Pokemon não encontrado'
        }
    }
})
def update_pokemon(pokemon_id):
    dados = request.get_json()
    if not dados or 'name' not in dados or 'captured' not in dados:
        return jsonify({'erro': 'Campos name e captured obrigatórios'}), 400

    for p in pokemons:
        if p['id'] == pokemon_id:
            p['name'] = dados['name']
            p['captured'] = dados['captured']
            return jsonify(p), 200
    return jsonify({'erro': 'Pokémon não encontrado'}), 404


@app.route('/pokemons/<int:pokemon_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Pokemons'],
    'parameters': [
        {
            'name': 'pokemon_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do pokemon'
        }
    ],
    'responses': {
        204: {
            'description': 'Pokemon deletado com sucesso'
        },
        404: {
            'description': 'Pokemon não encontrado'
        }
    }
})
def delete_pokemon(pokemon_id):
    for i, p in enumerate(pokemons):
        if p['id'] == pokemon_id:
            pokemons.pop(i)
            return '', 204
    return jsonify({'erro': 'Pokémon não encontrado'}), 404


@app.route('/capture/<int:pokemon_id>', methods=['GET'])
@swag_from({
    'tags': ['Capture'],
    'parameters': [
        {
            'name': 'pokemon_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do pokemon que você quer tentar capturar'
        }
    ],
    'responses': {
        200: {
            'description': 'Resultado da tentativa de captura',
            'schema': {
                '$ref': '#/definitions/Pokemon'
            }
        },
        404: {
            'description': 'Pokemon não encontrado'
        }
    }
})
def capture_pokemon(pokemon_id):
    for p in pokemons:
        if p['id'] == pokemon_id:
            resultado = random.choice([True, False])
            p['captured'] = resultado
            return jsonify(p), 200
    return jsonify({'erro': 'Pokémon não encontrado'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
