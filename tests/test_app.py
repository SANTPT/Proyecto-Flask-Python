import os
import tempfile
import json
import pytest

from app import app
import database

@pytest.fixture
def client():
    # 1. Creamos un archivo temporal para que nuestras pruebas no
    # sobreescriban ni modifiquen tu 'database.db' real.
    db_fd, db_path = tempfile.mkstemp()
    
    # 2. Le decimos al código que use este archivo temporal
    database.DATABASE = db_path
    
    app.config['TESTING'] = True
    
    # 3. Inicializamos las tablas vacías en este archivo temporal
    with app.app_context():
        conn = database.get_db_connection()
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()
        
    # 4. Entregamos el cliente para que corra el test
    with app.test_client() as client:
        yield client
        
    # 5. Limpieza: al terminar el test, borramos la base de datos temporal
    os.close(db_fd)
    os.unlink(db_path)


# --- PRUEBAS GLOBALES (E2E / Integración) ---

def test_ruta_principal(client):
    """Verifica que el HTML principal carga código 200."""
    response = client.get('/')
    assert response.status_code == 200


def test_api_crear_y_obtener_pelicula(client):
    """Verifica la creación mediante POST y la lectura mediante GET (Comportamiento Global)."""
    # 1. Intentamos crear una película nueva (POST)
    nueva_pelicula = {
        "titulo": "Inception",
        "genero": "Ciencia Ficción"
    }
    response_post = client.post(
        '/peliculas', 
        data=json.dumps(nueva_pelicula), 
        content_type='application/json'
    )
    assert response_post.status_code == 201
    
    # Validamos el mensaje de retorno
    data_post = response_post.get_json()
    assert data_post["mensaje"] == "Pelicula agregada"

    # 2. Obtenemos todas las películas (GET global)
    response_get = client.get('/peliculas')
    assert response_get.status_code == 200
    
    peliculas = response_get.get_json()
    # Sabemos que la DB estaba vacía, así que debe haber exactamente 1 película
    assert len(peliculas) == 1
    assert peliculas[0]["titulo"] == "Inception"
    assert peliculas[0]["genero"] == "Ciencia Ficción"


def test_api_actualizar_estado_pelicula(client):
    """Verifica el endpoint PUT para marcar como vista y calificar."""
    # Primero creamos una peli insertándola directo (Podríamos usar el endpoint como antes)
    client.post('/peliculas', data=json.dumps({"titulo": "Matrix", "genero": "Sci-Fi"}), content_type='application/json')
    
    # Actualizamos: marcamos como vista y le damos puntuación
    update_data = {
        "vista": True,
        "puntuacion": 5
    }
    response_put = client.put(
        '/peliculas/1', # La ID será 1 porque es la primera película en nuestra DB temporal
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response_put.status_code == 200
    
    # Comprobamos trayéndola sola
    response_get = client.get('/peliculas/1')
    peli_actualizada = response_get.get_json()
    
    assert peli_actualizada["vista"] == 1
    assert peli_actualizada["puntuacion"] == 5


def test_api_eliminar_pelicula(client):
    """Verifica que se pueda eliminar una película."""
    # Creamos
    client.post('/peliculas', data=json.dumps({"titulo": "Titanic", "genero": "Drama"}), content_type='application/json')
    
    # Eliminamos
    response_delete = client.delete('/peliculas/1')
    assert response_delete.status_code == 200
    
    # Comprobamos que ya no existe (la base de datos debe devolver lista vacía globalmente)
    peliculas_actuales = client.get('/peliculas').get_json()
    assert len(peliculas_actuales) == 0
