from flask import Blueprint, render_template, request, redirect, url_for
from services.peliculas_service import (
    obtener_peliculas,
    agregar_pelicula,
    eliminar_pelicula,
    marcar_como_vista,
    calificar_pelicula
)

peliculas_bp = Blueprint('peliculas', __name__)


@peliculas_bp.route('/')
def index():
    peliculas = obtener_peliculas()
    return render_template('index.html', peliculas=peliculas)


@peliculas_bp.route('/add', methods=['POST'])
def add():
    titulo = request.form['titulo']
    genero = request.form['genero']

    agregar_pelicula(titulo, genero)
    return redirect(url_for('peliculas.index'))


@peliculas_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    eliminar_pelicula(id)
    return redirect(url_for('peliculas.index'))


@peliculas_bp.route('/watch/<int:id>')
def watch(id):
    marcar_como_vista(id)
    return redirect(url_for('peliculas.index'))


@peliculas_bp.route('/rate/<int:id>', methods=['POST'])
def rate(id):
    puntuacion = request.form['puntuacion']

    calificar_pelicula(id, puntuacion)
    return redirect(url_for('peliculas.index'))