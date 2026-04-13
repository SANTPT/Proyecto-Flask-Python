from flask import Flask
from routes.peliculas import peliculas_bp
from seed import seed_data


def create_app(init_database=False, test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        APP_NAME="Movie Tracker",
    )

    if test_config:
        app.config.update(test_config)

    if init_database:
        init_db(force=app.config.get("FORCE_INIT_DB", False))

    app.register_blueprint(peliculas_bp)

if __name__ == '__main__':
    app.run(debug=True)
