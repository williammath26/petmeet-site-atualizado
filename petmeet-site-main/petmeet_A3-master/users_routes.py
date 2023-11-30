from flask_restx import Resource
from api import api_pet_meet
from auth import *
import bcrypt
import sqlite3


def register_users_routes(app):
    _, pet, pet_parser, cursor, conn, api, ns_users, user_parser, login_parser, user, association = api_pet_meet(
        app)

    @ns_users.route('/')
    class UserList(Resource):
        @ns_users.marshal_list_with(user)
        def get(self):
            """Listar todos os usuários"""
            cursor.execute("SELECT * FROM Usuario")
            users = cursor.fetchall()
            user_list = [{'ID': user[0], 'Nome': user[1],
                          'Email': user[2], 'Senha': user[3]} for user in users]
            return user_list

    @ns_users.route('/<int:id>')
    class PetItem(Resource):
        @ns_users.marshal_with(user)
        def get(self, id):
            """Listar usuário por ID"""
            cursor.execute("SELECT * FROM Usuario WHERE ID=?", (id,))
            user = cursor.fetchone()
            if user:
                return {'ID': user[0], 'Nome': user[1], 'Email': user[2], 'Senha': user[3]}
            api.abort(404, "User with ID {} doesn't exist".format(id))

    @ns_users.route('/<int:user_id>/associate-pet/<int:pet_id>')
    class AssociatePet(Resource):
        @ns_users.expect(association, validate=True)
        @ns_users.marshal_with(association, code=201)
        def post(self, user_id, pet_id):
            """Associar um pet a um usuário já existente (NÃO USAR)"""
            if user_token is not None:
                args = api.payload
                cursor.execute("SELECT * FROM Usuario WHERE ID=?", (user_id,))
                user = cursor.fetchone()
                cursor.execute("SELECT * FROM Pet WHERE ID=?", (pet_id,))
                pet = cursor.fetchone()
                if not user:
                    api.abort(
                        404, "User with ID {} doesn't exist".format(user_id))
                if not pet:
                    api.abort(
                        404, "Pet with ID {} doesn't exist".format(pet_id))
                cursor.execute(
                    "INSERT INTO PetUsuario (PetID, UsuarioID) VALUES (?, ?)", (user_id, pet_id))
                conn.commit()
                return {"UsuarioID": user_id, "PetID": pet_id}, 201
            else:
                return {'message': 'Access denied. Token is missing or invalid'}, 401

    @ns_users.route('/<int:user_id>/pets')
    class UserPets(Resource):
        @ns_users.marshal_list_with(pet)
        def get(self, user_id):
            """Listar usuário e seus pets (PRECISA DE LOGIN)"""
            if user_token is not None:
                cursor.execute("SELECT * FROM Usuario WHERE ID=?", (user_id,))
                user = cursor.fetchone()
            else:
                return {'message': 'Access denied. Token is missing or invalid'}, 401
            if not user:
                api.abort(404, "User with ID {} doesn't exist".format(user_id))

            cursor.execute(
                "SELECT * FROM Pet WHERE ID IN (SELECT PetID FROM PetUsuario WHERE UsuarioID=?)", (user_id,))
            pets = cursor.fetchall()

            pet_list = [{'ID': pet[0], 'Nome': pet[1], 'Especie': pet[2], 'Raca': pet[3], 'Genero': pet[4],
                         'DataNascimento': pet[5], 'Cor': pet[6], 'Peso': pet[7], 'Imagem': pet[8], 'Notas': pet[9],
                         'Vacinacao': pet[10], 'Medicamentos': pet[11], 'UltimaConsulta': pet[12],
                         'Veterinario': pet[13], 'HistoricoSaude': pet[14], 'Alimentacao': pet[15],
                         'Comportamento': pet[16]} for pet in pets]
            return pet_list

    @ns_users.route('/<int:user_id>/create-pet')
    class CreateUserPet(Resource):
        @ns_users.expect(pet, validate=True)
        @ns_users.marshal_with(pet, code=201)
        def post(self, user_id):
            """Adicionar PET a um usuário (PRECISA DE LOGIN)"""
            if user_token is not None:
                args = pet_parser.parse_args()
                cursor.execute("SELECT * FROM Usuario WHERE ID=?", (user_id,))
                user = cursor.fetchone()
                if not user:
                    api.abort(
                        404, "User with ID {} doesn't exist".format(user_id))

                cursor.execute("INSERT INTO Pet (Nome, Especie, Raca, Genero, DataNascimento, Cor, Peso, Imagem, Notas, Vacinacao, Medicamentos, UltimaConsulta, Veterinario, HistoricoSaude, Alimentacao, Comportamento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (args['Nome'], args['Especie'], args['Raca'], args['Genero'], args['DataNascimento'],
                                args['Cor'], args['Peso'], args['Imagem'], args['Notas'], args['Vacinacao'],
                                args['Medicamentos'], args['UltimaConsulta'], args['Veterinario'],
                                args['HistoricoSaude'], args['Alimentacao'], args['Comportamento']))
                conn.commit()
                new_pet_id = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO PetUsuario (PetID, UsuarioID) VALUES (?, ?)", (new_pet_id, user_id))
                conn.commit()

                return {"ID": new_pet_id, "Nome": args['Nome'], "Especie": args['Especie'],
                        "Raca": args['Raca'], "Genero": args['Genero'], "DataNascimento": args['DataNascimento'],
                        "Cor": args['Cor'], "Peso": args['Peso'], "Imagem": args['Imagem'], "Notas": args['Notas'],
                        "Vacinacao": args['Vacinacao'], "Medicamentos": args['Medicamentos'],
                        "UltimaConsulta": args['UltimaConsulta'], "Veterinario": args['Veterinario'],
                        "HistoricoSaude": args['HistoricoSaude'], "Alimentacao": args['Alimentacao'],
                        "Comportamento": args['Comportamento']}, 201
            else:
                return {'message': 'Access denied. Token is missing or invalid'}, 401

    @ns_users.route('/<int:user_id>/update-pet/<int:pet_id>')
    class UpdateUserPet(Resource):
        @ns_users.expect(pet, validate=True)
        @ns_users.marshal_with(pet)
        def put(self, user_id, pet_id):
            """Atualizar dados de pet associado a usuário (PRECIA DE LOGIN)"""
            if user_token is not None:
                args = pet_parser.parse_args()
                cursor.execute("SELECT * FROM Usuario WHERE ID=?", (user_id,))
                user = cursor.fetchone()
                if not user:
                    api.abort(
                        404, "User with ID {} doesn't exist".format(user_id))

                cursor.execute("UPDATE Pet SET Nome=?, Especie=?, Raca=?, Genero=?, DataNascimento=?, Cor=?, Peso=?, Imagem=?, Notas=?, Vacinacao=?, Medicamentos=?, UltimaConsulta=?, Veterinario=?, HistoricoSaude=?, Alimentacao=?, Comportamento=? WHERE ID=?",
                               (args['Nome'], args['Especie'], args['Raca'], args['Genero'], args['DataNascimento'],
                                args['Cor'], args['Peso'], args['Imagem'], args['Notas'], args['Vacinacao'],
                                args['Medicamentos'], args['UltimaConsulta'], args['Veterinario'],
                                args['HistoricoSaude'], args['Alimentacao'], args['Comportamento'], pet_id))
                conn.commit()

                return {"ID": pet_id, "Nome": args['Nome'], "Especie": args['Especie'],
                        "Raca": args['Raca'], "Genero": args['Genero'], "DataNascimento": args['DataNascimento'],
                        "Cor": args['Cor'], "Peso": args['Peso'], "Imagem": args['Imagem'], "Notas": args['Notas'],
                        "Vacinacao": args['Vacinacao'], "Medicamentos": args['Medicamentos'],
                        "UltimaConsulta": args['UltimaConsulta'], "Veterinario": args['Veterinario'],
                        "HistoricoSaude": args['HistoricoSaude'], "Alimentacao": args['Alimentacao'],
                        "Comportamento": args['Comportamento']}
            else:
                return {'message': 'Access denied. Token is missing or invalid'}, 401

    @ns_users.route('/<int:user_id>/delete-pet/<int:pet_id>')
    class DeleteUserPet(Resource):
        @ns_users.doc(responses={204: "Pet deleted"})
        def delete(self, user_id, pet_id):
            """Deletar PET associado a usuário (PRECISA DE LOGIN)"""
            try:
                if user_token is not None:
                    # Verificar se o usuário existe antes de proceder com a exclusão do pet
                    cursor.execute("SELECT * FROM Usuario WHERE ID=?", (user_id,))
                    user = cursor.fetchone()
                    if not user:
                        return {'message': f'User with ID {user_id} does not exist'}, 404

                    # Verificar se o pet está associado a esse usuário
                    cursor.execute("SELECT * FROM PetUsuario WHERE UsuarioID=? AND PetID=?", (user_id, pet_id))
                    pet_user_association = cursor.fetchone()
                    if not pet_user_association:
                        return {'message': f'Pet with ID {pet_id} is not associated with User ID {user_id}'}, 404

                    # Verificar se o pet não está associado a nenhum outro usuário
                    cursor.execute("SELECT COUNT(*) FROM PetUsuario WHERE PetID=?", (pet_id,))
                    pet_count = cursor.fetchone()[0]

                    if pet_count == 1:
                        # Se o pet não estiver associado a nenhum outro usuário, exclua-o do banco de dados
                        cursor.execute("DELETE FROM Pet WHERE ID=?", (pet_id,))
                        conn.commit()
                        return {'message': 'Pet deleted successfully.'}, 204

                    # Se o pet estiver associado a outros usuários, apenas remova a associação com o usuário atual
                    cursor.execute("DELETE FROM PetUsuario WHERE UsuarioID=? AND PetID=?", (user_id, pet_id))
                    conn.commit()
                    return {'message': 'Pet association removed from user successfully.'}, 204

                else:
                    return {'message': 'Access denied. Token is missing or invalid'}, 401

            except sqlite3.Error as e:
                conn.rollback()
                return {'message': f'Error deleting pet: {str(e)}'}, 500


    @ns_users.route('/login')
    class Login(Resource):
        @ns_users.expect(login_parser, validate=True)
        def post(self):
            """Fazer Login"""
            args = login_parser.parse_args()
            user_email = args['Email']
            user_password = args['Senha']
            cursor.execute(
                "SELECT * FROM Usuario WHERE Email=?", (user_email,))
            user = cursor.fetchone()

            if user:
                stored_password = user[3]
                if bcrypt.checkpw(user_password.encode('utf-8'), stored_password):
                    user_id = user[0]
                    user_token = generate_token(user_id)
                    user_name = user[1]  # Adicione esta linha para obter o nome do usuário
                    return {'access_token': user_token, 'user_name': user_name, 'message': 'Login successful'}, 200

            return {'message': 'Login failed. Check your email and password.'}, 401

    @ns_users.route('/create')
    class CreateUser(Resource):
        @ns_users.expect(user, validate=True)
        @ns_users.marshal_with(user, code=201)
        def post(self):
            """Criar novo usuário"""
            args = user_parser.parse_args()
            cursor.execute(
                "SELECT ID FROM Usuario WHERE Email=?", (args['Email'],))
            existing_user = cursor.fetchone()

            if existing_user:
                return {'message': 'User with the same email already exists'}, 400

            hashed_password = bcrypt.hashpw(
                args['Senha'].encode('utf-8'), bcrypt.gensalt())
            user_data = (args['Nome'], args['Email'], hashed_password)

            cursor.execute(
                "INSERT INTO Usuario (Nome, Email, Senha) VALUES (?, ?, ?)", user_data)
            conn.commit()

            new_user_id = cursor.lastrowid
            new_user = {
                'ID': new_user_id,
                'Nome': args['Nome'],
                'Email': args['Email']
            }

            return new_user, 201

    @ns_users.route('/all-users-and-pets')
    class AllUsersPets(Resource):
        def get(self):
            """Listar todos os usuários e seus pets"""
            cursor.execute(
                "SELECT u.ID, u.Nome, u.Email, p.ID, p.Nome AS PetNome, p.Especie FROM Usuario u LEFT JOIN PetUsuario pu ON u.ID = pu.UsuarioID LEFT JOIN Pet p ON pu.PetID = p.ID")
            user_pet_data = cursor.fetchall()

            users_pets_dict = {}
            for row in user_pet_data:
                user_id = row[0]
                user_name = row[1]
                user_email = row[2]
                pet_id = row[3]
                pet_name = row[4]
                pet_species = row[5]

                if user_id not in users_pets_dict:
                    users_pets_dict[user_id] = {
                        'ID': user_id,
                        'Nome': user_name,
                        'Email': user_email,
                        'Pets': []
                    }

                if pet_id is not None:
                    users_pets_dict[user_id]['Pets'].append({
                        'ID': pet_id,
                        'Nome': pet_name,
                        'Especie': pet_species
                    })

            users_pets_list = list(users_pets_dict.values())
            return users_pets_list
