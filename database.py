import sqlite3
import os

DATABASE = os.environ.get('DATABASE_NAME', 'database.db')

def get_db_connection(db_path=None):
    """Establece una conexión con la base de datos SQLite."""
    if db_path is None:
        db_path = DATABASE
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos si no existe o si se requiere recrear las tablas."""
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.close()
        print("Base de datos inicializada correctamente.")
