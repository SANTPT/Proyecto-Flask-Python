

from flask import Flask

import os
import time
from datetime import datetime

from flask import Flask, g, render_template, request

from database import init_db

from routes.peliculas import peliculas_bp
from seed import seed_data


def create_app(init_database=False, test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        APP_NAME="Movie Tracker",
    )

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=True)

=======
    if test_config:
        app.config.update(test_config)

    if init_database:
        init_db(force=app.config.get("FORCE_INIT_DB", False))

    app.register_blueprint(peliculas_bp)

    @app.before_request
    def before_request_logging():
        g.request_started_at = time.perf_counter()
        g.request_path = request.path
        g.request_method = request.method
        app.logger.info("Inicio request: %s %s", request.method, request.path)

    @app.after_request
    def after_request_logging(response):
        response.headers["X-App-Name"] = app.config.get("APP_NAME", "Flask App")

        started_at = getattr(g, "request_started_at", None)
        if started_at is not None:
            elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)
            response.headers["X-Request-Duration-ms"] = str(elapsed_ms)
            app.logger.info(
                "Fin request: %s %s -> %s (%sms)",
                request.method,
                request.path,
                response.status_code,
                elapsed_ms,
            )

        return response

    @app.teardown_request
    def teardown_request_logging(error=None):
        if error is not None:
            app.logger.exception(
                "Error en request: %s %s | %s",
                getattr(g, "request_method", "UNKNOWN"),
                getattr(g, "request_path", "UNKNOWN"),
                error,
            )

    @app.context_processor
    def inject_global_template_vars():
        return {
            "app_name": app.config.get("APP_NAME", "Movie Tracker"),
            "current_year": datetime.now().year,
        }

    @app.template_filter("movie_status")
    def movie_status_filter(vista):
        return "VIEWED" if vista else "PENDING"

    @app.template_test("rated")
    def is_rated(value):
        return isinstance(value, int) and 1 <= value <= 10

    @app.template_global("rating_badge")
    def rating_badge(score):
        if score is None:
            return "Sin calificar"
        if score >= 8:
            return "Excelente"
        if score >= 5:
            return "Aceptable"
        return "Baja"

    @app.errorhandler(400)
    def bad_request(error):
        message = getattr(error, "description", "La solicitud no es válida.")
        return render_template(
            "errors/400.html",
            title="Solicitud incorrecta",
            message=message,
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        message = getattr(error, "description", "El recurso solicitado no existe.")
        return render_template(
            "errors/404.html",
            title="Página no encontrada",
            message=message,
        ), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template(
            "errors/500.html",
            title="Error interno del servidor",
            message="Ocurrió un problema inesperado. Intenta nuevamente en unos momentos.",
        ), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = create_app(init_database=True, test_config={"FORCE_INIT_DB": False})
    seed_data()
    app.run(debug=True, port=port)
>>>>>>> 87c65063dc0e57a05fa79a3f6a53374fcbe7a2d0
