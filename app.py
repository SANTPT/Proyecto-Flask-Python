import os
from flask import Flask
from routes.peliculas import peliculas_bp
from database import init_db
from seed import seed_data


def create_app(init_database=False):
    app = Flask(__name__)

    app.register_blueprint(peliculas_bp)

    if init_database:
        init_db()

    return app


# App para imports (tests, WSGI, etc.) sin efectos secundarios
app = create_app()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    # Inicialización controlada solo al ejecutar la app directamente
    app = create_app(init_database=True)

    # Cargar seed automáticamente al arrancar
    seed_data(force=True)

    app.run(debug=True, port=port)