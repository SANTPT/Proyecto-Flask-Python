import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def seed_data():
    conn = get_db_connection()
    
    # 1. Limpiar tabla para evitar duplicados
    conn.execute('DELETE FROM peliculas')
    
    # 2. Películas con géneros variados para ver el diseño
    peliculas = [
        ('SEVEN SAMURAI', 'DRAMA', 1, 9),
        ('BLADE RUNNER', 'SCI-FI', 1, 9),
        ('SPIRITED AWAY', 'ANIMATION', 1, 10),
        ('PARASITE', 'THRILLER', 1, 10),
        ('ALIEN', 'HORROR', 0, None),
        ('MAD MAX: FURY ROAD', 'ACTION', 1, 9),
        ('PULP FICTION', 'CRIME', 1, 10),
    ]
    
    # 3. Insertamos cada película una por una
    for peli in peliculas:
        # Usamos '?' para evitar inyecciones SQL de forma segura
        conn.execute(
            'INSERT INTO peliculas (titulo, genero, vista, puntuacion) VALUES (?, ?, ?, ?)',
            peli
        )
        
    # 4. Confirmar (commit) y cerrar conexión
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_data()
