from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from services.peliculas_service import (
    obtener_peliculas,
    obtener_pelicula_por_id,
    agregar_pelicula,
    eliminar_pelicula,
    marcar_como_vista,
    calificar_pelicula,
)
from utils.decorators import (
    validate_movie_form_fields,
    validate_rating_field,
    movie_must_exist,
    log_action,
)

peliculas_bp = Blueprint("peliculas", __name__)


@peliculas_bp.route("/", methods=["GET"])
def index():
    peliculas = obtener_peliculas()
    return render_template("index.html", peliculas=peliculas)


@peliculas_bp.route("/add", methods=["POST"])
@log_action("agregar_pelicula")
def add():
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
        titulo = data.get("titulo", "").strip()
        genero = data.get("genero", "").strip()
    else:
        titulo = request.form.get("titulo", "").strip()
        genero = request.form.get("genero", "").strip()

    # Validation
    if not titulo or not genero:
        if request.is_json:
            return jsonify({"error": "titulo y genero son requeridos"}), 400
        abort(400, description="Faltan campos obligatorios: titulo, genero")

    agregar_pelicula(titulo, genero)

    if request.is_json:
        return jsonify({"mensaje": "Película agregada"}), 201
    return redirect(url_for("peliculas.index"))


@peliculas_bp.route("/delete/<int:id>", methods=["POST"])
@log_action("eliminar_pelicula")
def delete(id):
    pelicula = obtener_pelicula_por_id(id)
    if pelicula is None:
        if request.is_json:
            return jsonify({"error": "Película no encontrada"}), 404
        abort(404, description="La película solicitada no existe.")

    eliminar_pelicula(id)

    if request.is_json:
        return jsonify({"mensaje": "Película eliminada"})
    return redirect(url_for("peliculas.index"))


@peliculas_bp.route("/watch/<int:id>", methods=["POST"])
@log_action("marcar_como_vista")
def watch(id):
    pelicula = obtener_pelicula_por_id(id)
    if pelicula is None:
        if request.is_json:
            return jsonify({"error": "Película no encontrada"}), 404
        abort(404, description="La película solicitada no existe.")

    marcar_como_vista(id)

    if request.is_json:
        return jsonify({"mensaje": "Película marcada como vista"})
    return redirect(url_for("peliculas.index"))


@peliculas_bp.route("/rate/<int:id>", methods=["POST"])
@log_action("calificar_pelicula")
def rate(id):
    pelicula = obtener_pelicula_por_id(id)
    if pelicula is None:
        if request.is_json:
            return jsonify({"error": "Película no encontrada"}), 404
        abort(404, description="La película solicitada no existe.")

    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
        puntuacion_str = str(data.get("puntuacion", "")).strip()
    else:
        puntuacion_str = request.form.get("puntuacion", "").strip()

    # Validation
    if not puntuacion_str:
        if request.is_json:
            return jsonify({"error": "puntuacion es requerida"}), 400
        abort(400, description="La puntuación es obligatoria.")

    try:
        puntuacion = int(puntuacion_str)
    except ValueError:
        if request.is_json:
            return jsonify({"error": "puntuacion debe ser un número"}), 400
        abort(400, description="La puntuación debe ser un número entero.")

    if puntuacion < 1 or puntuacion > 10:
        if request.is_json:
            return jsonify({"error": "puntuacion debe estar entre 1 y 10"}), 400
        abort(400, description="La puntuación debe estar entre 1 y 10.")

    calificar_pelicula(id, puntuacion)

    if request.is_json:
        return jsonify({"mensaje": "Película calificada"})
    return redirect(url_for("peliculas.index"))
