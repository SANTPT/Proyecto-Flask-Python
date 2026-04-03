from functools import wraps

from flask import abort, current_app, request

from services.peliculas_service import obtener_pelicula_por_id


def validate_movie_form_fields(*required_fields):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            missing_fields = []

            for field in required_fields:
                value = request.form.get(field, "").strip()
                if not value:
                    missing_fields.append(field)

            if missing_fields:
                abort(
                    400,
                    description="Faltan campos obligatorios: " + ", ".join(missing_fields),
                )

            return view_func(*args, **kwargs)

        return wrapper

    return decorator


def validate_rating_field(field_name="puntuacion", min_value=1, max_value=10):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            raw_value = request.form.get(field_name, "").strip()

            if not raw_value:
                abort(400, description="La puntuación es obligatoria.")

            try:
                score = int(raw_value)
            except ValueError:
                abort(400, description="La puntuación debe ser un número entero.")

            if score < min_value or score > max_value:
                abort(
                    400,
                    description=f"La puntuación debe estar entre {min_value} y {max_value}.",
                )

            return view_func(*args, **kwargs)

        return wrapper

    return decorator


def movie_must_exist(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        movie_id = kwargs.get("id")

        if movie_id is None:
            abort(400, description="No se recibió el id de la película.")

        pelicula = obtener_pelicula_por_id(movie_id)

        if pelicula is None:
            abort(404, description="La película solicitada no existe.")

        return view_func(*args, **kwargs)

    return wrapper


def log_action(action_name=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            action = action_name or view_func.__name__

            current_app.logger.info(
                "Acción=%s | endpoint=%s | método=%s | ruta=%s | params=%s",
                action,
                request.endpoint,
                request.method,
                request.path,
                kwargs,
            )

            return view_func(*args, **kwargs)

        return wrapper

    return decorator