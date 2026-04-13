from flask import request, jsonify
from flask_cors import CORS
from services.peliculas_service import *

def init_routes(app):
    # Aplicamos CORS a la app si quieres que sea global
    CORS(app)

    @app.route("/") # Si me pides /
    def hello_root():
        return '<h1>Hola, este es el endpoint de la ruta raiz de Proyecto Flask 2</h1>'

    @app.route("/peliculas", methods=['GET']) # Si me pides /peliculas con GET
    def get_peliculas():
        return jsonify(obtener_peliculas())

    @app.route("/peliculas/<id>", methods=['GET']) # Si me pides /peliculas/id con GET
    def get_pelicula(id):
        return jsonify(obtener_pelicula_por_id(id))

    @app.route("/peliculas", methods=["POST"]) # Si me pides /peliculas con POST
    def new_pelicula():
        data = request.get_json()
        print('**new_movie', data)
        agregar_pelicula(data['titulo'], data['genero'])
        return jsonify({"mensaje": "Pelicula agregada"}), 201

    @app.route("/peliculas/<id>", methods=["PUT"]) # Si me pides /peliculas/id con PUT
    def update_pelicula(id):
        data = request.get_json()
        print('**update_movie', id)
        if 'puntuacion' in data:
            calificar_pelicula(id, data['puntuacion'])
        if 'vista' in data:
            marcar_como_vista(id)
        return jsonify({"mensaje": "Pelicula actualizada"})

    @app.route("/peliculas/<id>", methods=['DELETE']) # Si me pides /peliculas/id con DELETE
    def delete_pelicula(id):
        eliminar_pelicula(id)
        return jsonify({"mensaje": "Pelicula eliminada"})
