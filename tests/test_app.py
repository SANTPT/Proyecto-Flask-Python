import os
import tempfile
import json
import pytest

from app import app
import database

@pytest.fixture
def client():
    """Configuración del entorno de pruebas."""
    db_fd, db_path = tempfile.mkstemp()
    database.DATABASE = db_path
    app.config['TESTING'] = True
    
    with app.app_context():
        conn = database.get_db_connection()
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()
        
    with app.test_client() as client:
        yield client
        
    os.close(db_fd)
    os.unlink(db_path)

# --- tests ---

def test_cargar_pagina_principal(client):
    """1. Verifica que la página de inicio cargue correctamente (Código 200)."""
    response = client.get('/')
    assert response.status_code == 200

def test_agregar_pelicula(client):
    """2. Verifica que se pueda agregar una película nueva mediante la API."""
    nueva_peli = {"titulo": "Interstellar", "genero": "Ciencia Ficción"}
    
    response = client.post(
        '/peliculas', 
        data=json.dumps(nueva_peli), 
        content_type='application/json'
    )
    
    # Comprobamos que se creó (201) y que el mensaje es correcto
    assert response.status_code == 201
    assert response.get_json()["mensaje"] == "Pelicula agregada"

def test_eliminar_pelicula(client):
    """3. Verifica que se pueda borrar una película de la lista."""
    # Primero agregamos una para tener qué borrar
    client.post('/peliculas', data=json.dumps({"titulo": "Avatar", "genero": "Accion"}), content_type='application/json')
    
    # Intentamos borrar la película con ID 1
    response = client.delete('/peliculas/1')
    
    assert response.status_code == 200
    assert response.get_json()["mensaje"] == "Pelicula eliminada"
