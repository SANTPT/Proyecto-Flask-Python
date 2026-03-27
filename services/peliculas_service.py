import sqlite3


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def obtener_peliculas():
    conn = get_db_connection()
    peliculas = conn.execute('SELECT * FROM peliculas').fetchall()
    conn.close()
    return peliculas


def agregar_pelicula(titulo, genero):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO peliculas (titulo, genero) VALUES (?, ?)',
        (titulo, genero)
    )
    conn.commit()
    conn.close()


def eliminar_pelicula(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM peliculas WHERE id = ?', (id,))
    conn.commit()
    conn.close()


def marcar_como_vista(id):
    conn = get_db_connection()
    conn.execute(
        'UPDATE peliculas SET vista = 1 WHERE id = ?',
        (id,)
    )
    conn.commit()
    conn.close()


def calificar_pelicula(id, puntuacion):
    conn = get_db_connection()
    conn.execute(
        'UPDATE peliculas SET puntuacion = ? WHERE id = ?',
        (puntuacion, id)
    )
    conn.commit()
    conn.close()
