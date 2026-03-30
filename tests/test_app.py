import pytest
import os
from app import app
from database import get_db_connection

TEST_DB = 'test_database.db'

@pytest.fixture(scope='module', autouse=True)
def setup_database():
    """Crea e inicializa una base de datos de prueba."""
    # Configurar la variable de entorno para que el resto de la app la use
    os.environ['DATABASE_NAME'] = TEST_DB
    
    conn = get_db_connection(TEST_DB)
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    
    # Agregar una película inicial para los tests que la necesiten
    conn.execute("INSERT INTO peliculas (titulo, genero) VALUES ('Inception', 'Sci-Fi')")
    conn.commit()
    conn.close()
    
    yield
    
    # Limpieza después de los tests
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route returns 200 and has the title."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'MOVIE TRACKER' in response.data

def test_add_movie(client):
    """Test adding a movie via POST."""
    response = client.post('/add', data={
        'titulo': 'The Matrix',
        'genero': 'Action'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'THE MATRIX' in response.data

def test_mark_watched(client):
    """Test marking a movie as watched."""
    conn = get_db_connection(TEST_DB)
    res = conn.execute("SELECT id FROM peliculas LIMIT 1").fetchone()
    movie_id = res['id']
    conn.close()
    
    response = client.get(f'/watch/{movie_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'VIEWED' in response.data

def test_rate_movie(client):
    """Test rating a movie."""
    conn = get_db_connection(TEST_DB)
    res = conn.execute("SELECT id FROM peliculas LIMIT 1").fetchone()
    movie_id = res['id']
    conn.close()
    
    response = client.post(f'/rate/{movie_id}', data={
        'puntuacion': '8'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'8' in response.data