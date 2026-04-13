from database import get_db_connection


def obtener_peliculas():
    conn = get_db_connection()
    peliculas = conn.execute("SELECT * FROM peliculas ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(ix) for ix in peliculas]


def obtener_pelicula_por_id(id):
    conn = get_db_connection()
    pelicula = conn.execute('SELECT * FROM peliculas WHERE id = ?', (id,)).fetchone()
    conn.close()
    return dict(pelicula) if pelicula else None


def agregar_pelicula(titulo, genero):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO peliculas (titulo, genero) VALUES (?, ?)",
        (titulo, genero),
    )
    conn.commit()
    conn.close()


def eliminar_pelicula(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM peliculas WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def marcar_como_vista(id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE peliculas SET vista = 1 WHERE id = ?",
        (id,),
    )
    conn.commit()
    conn.close()


def calificar_pelicula(id, puntuacion):
    conn = get_db_connection()
    conn.execute(
        "UPDATE peliculas SET puntuacion = ? WHERE id = ?",
        (int(puntuacion), id),
    )
    conn.commit()
    conn.close()