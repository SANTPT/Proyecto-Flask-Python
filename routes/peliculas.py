from flask import render_template, request, jsonify
from flask_cors import CORS
from services.peliculas_service import *

def init_routes(app):
    CORS(app)

    @app.route("/")
    def index():
        """Renderiza la página principal con la lista de películas."""
        return render_template('index.html', peliculas=obtener_peliculas())

    # --- CRUD JSON ORIGINAL ---

    @app.route("/peliculas", methods=['GET'])
    def get_peliculas():
        return jsonify(obtener_peliculas())

    @app.route("/peliculas/<id>", methods=['GET'])
    def get_pelicula(id):
        return jsonify(obtener_pelicula_por_id(id))

    @app.route("/peliculas", methods=["POST"])
    def new_pelicula():
        data = request.get_json()
        agregar_pelicula(data['titulo'], data['genero'])
        return jsonify({"mensaje": "Pelicula agregada"}), 201

    @app.route("/peliculas/<id>", methods=["PUT"])
    def update_pelicula(id):
        data = request.get_json()
        if data and 'puntuacion' in data:
            calificar_pelicula(id, data['puntuacion'])
        if data and 'vista' in data:
            marcar_como_vista(id)
        return jsonify({"mensaje": "Pelicula actualizada"})

    @app.route("/peliculas/<id>", methods=['DELETE'])
    def delete_pelicula(id):
        eliminar_pelicula(id)
        return jsonify({"mensaje": "Pelicula eliminada"})
