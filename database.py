import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATABASE = BASE_DIR / "database.db"


def get_database_path():
    return os.environ.get("DATABASE_NAME", str(DEFAULT_DATABASE))


def get_db_connection(db_path=None):
    if db_path is None:
        db_path = get_database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(force=False, db_path=None):
    if db_path is None:
        db_path = get_database_path()

    schema_path = BASE_DIR / "schema.sql"

    if force and os.path.exists(db_path):
        os.remove(db_path)

    if not os.path.exists(db_path):
        conn = get_db_connection(db_path)
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.close()
        print("Base de datos inicializada correctamente.")