from database import get_db_connection


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
    try:
        puntuacion_int = int(puntuacion)
    except (ValueError, TypeError):
        puntuacion_int = 0
    conn.execute(
        'UPDATE peliculas SET puntuacion = ? WHERE id = ?',
        (puntuacion_int, id)
    )
    conn.commit()
    conn.close()