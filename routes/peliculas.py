from flask import Blueprint, render_template, request, redirect, url_for

from services.peliculas_service import (
    obtener_peliculas,
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
@validate_movie_form_fields("titulo", "genero")
@log_action("agregar_pelicula")
def add():
    titulo = request.form.get("titulo", "").strip()
    genero = request.form.get("genero", "").strip()

    agregar_pelicula(titulo, genero)
    return redirect(url_for("peliculas.index"))


@peliculas_bp.route("/delete/<int:id>", methods=["POST"])
@movie_must_exist
@log_action("eliminar_pelicula")
def delete(id):
    eliminar_pelicula(id)
    return redirect(url_for("peliculas.index"))


@peliculas_bp.route("/watch/<int:id>", methods=["POST"])
@movie_must_exist
@log_action("marcar_como_vista")
def watch(id):
    marcar_como_vista(id)
    return redirect(url_for("peliculas.index"))


@peliculas_bp.route("/rate/<int:id>", methods=["POST"])
@movie_must_exist
@validate_rating_field()
@log_action("calificar_pelicula")
def rate(id):
    puntuacion = int(request.form.get("puntuacion", "").strip())
    calificar_pelicula(id, puntuacion)
    return redirect(url_for("peliculas.index"))