from flask_restx import Resource
from api import api_pet_meet

def register_pet_routes(app):
     
    ns_pets, pet, pet_parser, cursor, conn, api, _, _, _, _, _ = api_pet_meet(app)


    # Endpoint para adcionar novo pet

    @ns_pets.route('/add')
    class AddPet(Resource):
        @ns_pets.expect(pet, validate=True)
        @ns_pets.marshal_with(pet, code=201)
        def post(self):
            """Add a new pet"""
            args = pet_parser.parse_args()
            cursor.execute("INSERT INTO Pet (Nome, Especie) VALUES (?, ?)",
                           (args['Nome'], args['Especie']))
            conn.commit()
            new_pet_id = cursor.lastrowid
            return {'ID': new_pet_id, 'Nome': args['Nome'], 'Especie': args['Especie']}, 201

        # Endpoint para detalhes de pet um por ID
        @ns_pets.route('/<int:id>')
        class PetItem(Resource):
            @ns_pets.marshal_with(pet)
            def get(self, id):
                """Get details of a specific pet"""
                cursor.execute("SELECT * FROM Pet WHERE ID=?", (id,))
                pet = cursor.fetchone()
                if pet:
                    return {'ID': pet[0], 'Nome': pet[1], 'Especie': pet[2]}
                api.abort(404, "Pet with ID {} doesn't exist".format(id))

            @ns_pets.expect(pet, validate=True)
            @ns_pets.marshal_with(pet)
            def put(self, id):
                """Update details of a specific pet"""
                args = pet_parser.parse_args()
                cursor.execute("UPDATE Pet SET Nome=?, Especie=? WHERE ID=?",
                               (args['Nome'], args['Especie'], id))
                conn.commit()
                cursor.execute("SELECT * FROM Pet WHERE ID=?", (id,))
                pet = cursor.fetchone()
                if pet:
                    return {'ID': pet[0], 'Nome': pet[1], 'Especie': pet[2]}
                api.abort(404, "Pet with ID {} doesn't exist".format(id))

            @ns_pets.doc(params={'id': 'ID of the pet to be deleted'})
            @ns_pets.doc(responses={204: "Pet deleted"})
            def delete(self, id):
                """Delete a specific pet"""
                cursor.execute("SELECT * FROM Pet WHERE ID=?", (id,))
                pet = cursor.fetchone()

                if pet:
                    cursor.execute("DELETE FROM Pet WHERE ID=?", (id,))
                    conn.commit()
                    return '', 204  # Retornar 204 se o pet foi excluído com sucesso
                else:
                    # Se o pet não existe, retornar erro 404
                    api.abort(404, "Pet with ID {} not found".format(id))

             # Endpoint para listar todos os pets
            @ns_pets.route('/')
            class PetList(Resource):
                @ns_pets.marshal_list_with(pet)
                def get(self):
                    """List all Pets"""
                    cursor.execute("SELECT * FROM Pet")
                    pets = cursor.fetchall()
                    pet_list = [{'ID': pet[0], 'Nome': pet[1], 'Especie': pet[2]}
                                for pet in pets]
                    return pet_list
