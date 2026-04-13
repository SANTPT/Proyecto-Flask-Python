from flask import jsonify, request, render_template
import datetime

def init_decorators(app):
    """Inicializa todos los decoradores (manejo de errores, callbacks, filtros de sesión)"""

    # --- 1. MANEJO DE ERRORES ---
    
    @app.errorhandler(400)
    def bad_request_error(e):
        return jsonify({"error": "Petición incorrecta. Revisa los datos enviados."}), 400

    @app.errorhandler(404)
    def resource_not_found_error(e):
        # Si la petición acepta JSON por encima de HTML (es una llamada API/Fetch)
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify({"error": "La ruta o película solicitada no fue encontrada."}), 404
        
        # Si es un usuario navegando de forma convencional
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify({"error": "Error interno del servidor."}), 500
            
        return render_template('500.html'), 500


    # --- 2. CALLBACKS DE PETICIÓN (BEFORE/AFTER REQUEST) ---
    
    @app.before_request
    def log_request_info():
        # Registramos qué se está pidiendo por consola (muy útil para depurar)
        print(f"[LOG] Recibida petición: {request.method} -> {request.path}")


    # --- 3. CONTEXTO DE PLANTILLAS Y FILTROS JINJA2 ---
    
    @app.context_processor
    def inject_global_vars():
        # Inyecta variables que estarán disponibles en todos los HTML
        return {
            "anio_actual": datetime.datetime.now().year,
            "nombre_app": "App de Películas"
        }

    @app.template_filter('mayusculas')
    def filter_mayusculas(texto):
        # Filtro de Jinja para poner textos en mayúscula
        return str(texto).upper() if texto else ""
