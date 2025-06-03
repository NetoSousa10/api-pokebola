from flask import Flask, jsonify
from flasgger import Swagger, swag_from
import random

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'API de Pokébola – Atividade Swagger',
    'uiversion': 3,
    'definitions': {
        'CaptureResponse': {
            'type': 'object',
            'properties': {
                'pokemon': {
                    'type': 'string',
                    'example': 'Pikachu'
                },
                'captured': {
                    'type': 'boolean',
                    'example': True
                }
            },
            'required': ['pokemon', 'captured']
        }
    }
}
Swagger(app)

POKEMONS = [
    "Pikachu",
    "Charmander",
    "Bulbasaur",
    "Squirtle",
    "Eevee",
    "Jigglypuff",
    "Pidgey",
    "Meowth"
]

@app.route('/capture', methods=['GET'])
@swag_from({
    'tags': ['Capture'],
    'responses': {
        200: {
            'description': 'Resultado da tentativa de captura de um Pokémon',
            'schema': {
                '$ref': '#/definitions/CaptureResponse'
            }
        }
    }
})
def capture():
    escolhido = random.choice(POKEMONS)
    capturado = random.choice([True, False])
    resultado = {
        "pokemon": escolhido,
        "captured": capturado
    }
    return jsonify(resultado), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
