from flask import Flask, jsonify, request, redirect, url_for
from flasgger import Swagger, swag_from
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import random

app = Flask(__name__)
app.config.update(
    {
        "SWAGGER": {
            "title": "API de Pokébola com JWT",
            "uiversion": 3,
            "definitions": {
                "Pokemon": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "name": {"type": "string", "example": "Pikachu"},
                        "captured": {"type": "boolean", "example": False},
                    },
                    "required": ["id", "name", "captured"],
                },
                "PokemonInput": {
                    "type": "object",
                    "properties": {"name": {"type": "string", "example": "Charmander"}},
                    "required": ["name"],
                },
                "Login": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "example": "user@example.com"},
                        "password": {"type": "string", "example": "senha123"},
                    },
                    "required": ["email", "password"],
                },
                "JWT": {
                    "type": "object",
                    "properties": {"access_token": {"type": "string"}},
                },
            },
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "Digite: Bearer <seu_token_aqui>",
                }
            },
        },
        "JWT_SECRET_KEY": "altere-essa-chave-para-uma-segura",
    }
)
Swagger(app)

jwt = JWTManager(app)

# Usuários exemplo (em memória)
users = {"user@example.com": "senha123"}


@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("flasgger.apidocs"))


@app.route("/login", methods=["POST"])
@swag_from(
    {
        "tags": ["Auth"],
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {"$ref": "#/definitions/Login"},
            }
        ],
        "responses": {
            200: {
                "description": "Login bem-sucedido retorna JWT",
                "schema": {"$ref": "#/definitions/JWT"},
            },
            401: {"description": "Credenciais inválidas"},
        },
    }
)
def login():
    dados = request.get_json()
    email = dados.get("email")
    senha = dados.get("password")
    if email in users and users[email] == senha:
        token = create_access_token(identity=email)
        return jsonify(access_token=token), 200
    return jsonify({"erro": "Credenciais inválidas"}), 401


pokemons = []
next_id = 1


@app.route("/pokemons", methods=["GET"])
@jwt_required()
@swag_from(
    {
        "tags": ["Pokemons"],
        "security": [{"Bearer": []}],
        "responses": {
            200: {
                "description": "Lista todos os pokemons",
                "schema": {"type": "array", "items": {"$ref": "#/definitions/Pokemon"}},
            }
        },
    }
)
def list_pokemons():
    return jsonify(pokemons), 200


@app.route("/pokemons/<int:pokemon_id>", methods=["GET"])
@jwt_required()
@swag_from(
    {
        "tags": ["Pokemons"],
        "security": [{"Bearer": []}],
        "parameters": [
            {"name": "pokemon_id", "in": "path", "type": "integer", "required": True}
        ],
        "responses": {
            200: {
                "description": "Retorna um pokemon pelo ID",
                "schema": {"$ref": "#/definitions/Pokemon"},
            },
            404: {"description": "Pokemon não encontrado"},
        },
    }
)
def get_pokemon(pokemon_id):
    for p in pokemons:
        if p["id"] == pokemon_id:
            return jsonify(p), 200
    return jsonify({"erro": "Pokémon não encontrado"}), 404


@app.route("/pokemons", methods=["POST"])
@jwt_required()
@swag_from(
    {
        "tags": ["Pokemons"],
        "security": [{"Bearer": []}],
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {"$ref": "#/definitions/PokemonInput"},
            }
        ],
        "responses": {
            201: {
                "description": "Pokemon criado com sucesso",
                "schema": {"$ref": "#/definitions/Pokemon"},
            },
            400: {"description": "Campo name é obrigatório"},
        },
    }
)
def create_pokemon():
    global next_id
    dados = request.get_json()
    if not dados or "name" not in dados:
        return jsonify({"erro": "Campo name é obrigatório"}), 400
    novo = {"id": next_id, "name": dados["name"], "captured": False}
    pokemons.append(novo)
    next_id += 1
    return jsonify(novo), 201


@app.route("/pokemons/<int:pokemon_id>", methods=["PUT"])
@jwt_required()
@swag_from(
    {
        "tags": ["Pokemons"],
        "security": [{"Bearer": []}],
        "parameters": [
            {"name": "pokemon_id", "in": "path", "type": "integer", "required": True},
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "captured": {"type": "boolean"},
                    },
                    "required": ["name", "captured"],
                },
            },
        ],
        "responses": {
            200: {
                "description": "Pokemon atualizado",
                "schema": {"$ref": "#/definitions/Pokemon"},
            },
            400: {"description": "Campos obrigatórios"},
            404: {"description": "Pokemon não encontrado"},
        },
    }
)
def update_pokemon(pokemon_id):
    dados = request.get_json()
    if not dados or "name" not in dados or "captured" not in dados:
        return jsonify({"erro": "Campos obrigatórios"}), 400
    for p in pokemons:
        if p["id"] == pokemon_id:
            p["name"] = dados["name"]
            p["captured"] = dados["captured"]
            return jsonify(p), 200
    return jsonify({"erro": "Pokémon não encontrado"}), 404


@app.route("/pokemons/<int:pokemon_id>", methods=["DELETE"])
@jwt_required()
@swag_from(
    {
        "tags": ["Pokemons"],
        "security": [{"Bearer": []}],
        "parameters": [
            {"name": "pokemon_id", "in": "path", "type": "integer", "required": True}
        ],
        "responses": {
            204: {"description": "Deletado com sucesso"},
            404: {"description": "Pokemon não encontrado"},
        },
    }
)
def delete_pokemon(pokemon_id):
    for i, p in enumerate(pokemons):
        if p["id"] == pokemon_id:
            pokemons.pop(i)
            return "", 204
    return jsonify({"erro": "Pokémon não encontrado"}), 404


@app.route("/capture/<int:pokemon_id>", methods=["GET"])
@jwt_required()
@swag_from(
    {
        "tags": ["Capture"],
        "security": [{"Bearer": []}],
        "parameters": [
            {"name": "pokemon_id", "in": "path", "type": "integer", "required": True}
        ],
        "responses": {
            200: {
                "description": "Tentativa de captura",
                "schema": {"$ref": "#/definitions/Pokemon"},
            },
            404: {"description": "Pokemon não encontrado"},
        },
    }
)
def capture_pokemon(pokemon_id):
    for p in pokemons:
        if p["id"] == pokemon_id:
            resultado = random.choice([True, False])
            p["captured"] = resultado
            return jsonify(p), 200
    return jsonify({"erro": "Pokémon não encontrado"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
