from flask_restx import Api, fields, reqparse
import sqlite3

def api_pet_meet(app):

# Database initialization
    conn = sqlite3.connect('app_pet_meet.db', check_same_thread=False)
    cursor = conn.cursor()

    # API initialization
    api = Api(
        app,
        version="1.0",
        title="Pet-Meet Management API",
        description="API for managing pets and users",
    )

    ns_pets = api.namespace("pets", description="Pet operations")
    ns_users = api.namespace("users", description="User operations")



    # Parser Pet
    pet_parser = reqparse.RequestParser()
    pet_parser.add_argument('Nome', type=str, required=True)
    pet_parser.add_argument('Especie', type=str, required=True)
    pet_parser.add_argument('Raca', type=str)
    pet_parser.add_argument('Genero', type=str)
    pet_parser.add_argument('DataNascimento', type=str)
    pet_parser.add_argument('Cor', type=str)
    pet_parser.add_argument('Peso', type=float)
    pet_parser.add_argument('Imagem', type=str)
    pet_parser.add_argument('Notas', type=str)
    pet_parser.add_argument('Vacinacao', type=str)
    pet_parser.add_argument('Medicamentos', type=str)
    pet_parser.add_argument('UltimaConsulta', type=str)
    pet_parser.add_argument('Veterinario', type=str)
    pet_parser.add_argument('HistoricoSaude', type=str)
    pet_parser.add_argument('Alimentacao', type=str)
    pet_parser.add_argument('Comportamento', type=str)

    # Login Parser
    login_parser = reqparse.RequestParser()
    login_parser.add_argument('Email', type=str, required=True)
    login_parser.add_argument('Senha', type=str, required=True)

    #User parser
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('Nome', type=str, required=True)
    user_parser.add_argument('Email', type=str, required=True)
    user_parser.add_argument('Senha', type=str, required=True)

        # Define the pet model
    pet = api.model(
    "Pet",
    {
        "ID": fields.Integer(readonly=True),
        "Nome": fields.String(required=True, description="Pet name"),
        "Especie": fields.String(required=True, description="Species"),
        "Raca": fields.String(description="Breed"),
        "Genero": fields.String(description="Gender"),
        "DataNascimento": fields.String(description="Date of Birth"),
        "Cor": fields.String(description="Color"),
        "Peso": fields.Float(description="Weight"),
        "Imagem": fields.String(description="Image address"),
        "Notas": fields.String(description="Notes"),
        "Vacinacao": fields.String(description="Vaccination"),
        "Medicamentos": fields.String(description="Medications"),
        "UltimaConsulta": fields.String(description="Last Consultation"),
        "Veterinario": fields.String(description="Veterinarian"),
        "HistoricoSaude": fields.String(description="Health History"),
        "Alimentacao": fields.String(description="Feeding"),
        "Comportamento": fields.String(description="Behavior"),
    },
)

    # Define the user model
    user = api.model(
        "User",
        {
            "ID": fields.Integer(readonly=True),
            "Nome": fields.String(required=True, description="User name"),
            "Email": fields.String(required=True, description="Email"),
            "Senha": fields.String(required=True, description="Password"),
        },
    )

    # Define the association model
    association = api.model(
        "Association",
        {
            "PetID": fields.Integer(required=True, description="Pet ID"),
            "UsuarioID": fields.Integer(required=True, description="User ID"),
        },
    )



    return ns_pets, pet, pet_parser, cursor, conn, api, ns_users, user_parser, login_parser, user, association