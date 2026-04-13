from pathlib import Path

import pytest

import database
from app import create_app
from database import get_db_connection


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _schema_path() -> Path:
    return _project_root() / "schema.sql"


def _init_test_db(db_path: str):
    conn = get_db_connection(db_path)
    with open(_schema_path(), "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.execute(
        "INSERT INTO peliculas (titulo, genero, vista, puntuacion) VALUES (?, ?, ?, ?)",
        ("Inception", "Sci-Fi", 0, None),
    )
    conn.commit()
    conn.close()


@pytest.fixture
def app_instance(tmp_path, monkeypatch):
    test_db = tmp_path / "test_database.db"

    monkeypatch.setenv("DATABASE_NAME", str(test_db))
    _init_test_db(str(test_db))

    app = create_app(
        test_config={
            "TESTING": True,
            "APP_NAME": "Movie Tracker Test",
        }
    )

    return app


@pytest.fixture
def client(app_instance):
    with app_instance.test_client() as client:
        yield client


@pytest.fixture
def test_db_path():
    return database.get_database_path()


def _get_first_movie_id(db_path: str) -> int:
    conn = get_db_connection(db_path)
    movie = conn.execute(
        "SELECT id FROM peliculas ORDER BY id ASC LIMIT 1"
    ).fetchone()
    conn.close()
    return movie["id"]


def _get_movie_by_title(db_path: str, titulo: str):
    conn = get_db_connection(db_path)
    movie = conn.execute(
        "SELECT * FROM peliculas WHERE titulo = ?",
        (titulo,),
    ).fetchone()
    conn.close()
    return movie


def test_index_route_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_includes_after_request_header(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("X-App-Name") in {"Movie Tracker", "Movie Tracker Test"}


def test_add_movie_via_post_works(client, test_db_path):
    response = client.post(
        "/add",
        data={
            "titulo": "The Matrix",
            "genero": "Action",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    movie = _get_movie_by_title(test_db_path, "The Matrix")
    assert movie is not None
    assert movie["genero"] == "Action"


def test_add_movie_missing_required_fields_returns_400(client):
    response = client.post(
        "/add",
        data={
            "titulo": "",
            "genero": "",
        },
        follow_redirects=False,
    )
    assert response.status_code == 400


def test_watch_movie_via_post_works(client, test_db_path):
    movie_id = _get_first_movie_id(test_db_path)

    response = client.post(f"/watch/{movie_id}", follow_redirects=True)
    assert response.status_code == 200

    conn = get_db_connection(test_db_path)
    movie = conn.execute(
        "SELECT vista FROM peliculas WHERE id = ?",
        (movie_id,),
    ).fetchone()
    conn.close()

    assert movie is not None
    assert movie["vista"] == 1


def test_delete_movie_via_post_works(client, test_db_path):
    conn = get_db_connection(test_db_path)
    conn.execute(
        "INSERT INTO peliculas (titulo, genero, vista, puntuacion) VALUES (?, ?, ?, ?)",
        ("Movie To Delete", "Drama", 0, None),
    )
    conn.commit()
    movie = conn.execute(
        "SELECT id FROM peliculas WHERE titulo = ?",
        ("Movie To Delete",),
    ).fetchone()
    conn.close()

    movie_id = movie["id"]

    response = client.post(f"/delete/{movie_id}", follow_redirects=True)
    assert response.status_code == 200

    conn = get_db_connection(test_db_path)
    deleted = conn.execute(
        "SELECT id FROM peliculas WHERE id = ?",
        (movie_id,),
    ).fetchone()
    conn.close()

    assert deleted is None


def test_rate_movie_via_post_works(client, test_db_path):
    movie_id = _get_first_movie_id(test_db_path)

    response = client.post(
        f"/rate/{movie_id}",
        data={"puntuacion": "8"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    conn = get_db_connection(test_db_path)
    movie = conn.execute(
        "SELECT puntuacion FROM peliculas WHERE id = ?",
        (movie_id,),
    ).fetchone()
    conn.close()

    assert movie is not None
    assert movie["puntuacion"] == 8


def test_rate_movie_missing_rating_returns_400(client, test_db_path):
    movie_id = _get_first_movie_id(test_db_path)

    response = client.post(
        f"/rate/{movie_id}",
        data={},
        follow_redirects=False,
    )
    assert response.status_code == 400


def test_rate_movie_invalid_rating_returns_400(client, test_db_path):
    movie_id = _get_first_movie_id(test_db_path)

    response = client.post(
        f"/rate/{movie_id}",
        data={"puntuacion": "abc"},
        follow_redirects=False,
    )
    assert response.status_code == 400


def test_nonexistent_route_returns_404(client):
    response = client.get("/ruta-que-no-existe")
    assert response.status_code == 404


def test_movie_must_exist_returns_404(client):
    response = client.post("/watch/999999", follow_redirects=False)
    assert response.status_code == 404


def test_get_not_allowed_on_mutating_routes(client, test_db_path):
    movie_id = _get_first_movie_id(test_db_path)

    response_add = client.get("/add")
    response_delete = client.get(f"/delete/{movie_id}")
    response_watch = client.get(f"/watch/{movie_id}")
    response_rate = client.get(f"/rate/{movie_id}")

    assert response_add.status_code == 405
    assert response_delete.status_code == 405
    assert response_watch.status_code == 405
    assert response_rate.status_code == 405
