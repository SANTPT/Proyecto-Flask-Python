import os
from flask import Flask
from routes.peliculas import init_routes
from database import init_db
from seed import seed_data
from utils.decorators import init_decorators
from flask import Flask, abort

app = Flask(__name__)

# Ruta temporal para probar nuestro Error 500
@app.route('/forzar-error')
def generar_error():
    abort(500)  # Esto engaña al sistema haciéndole creer que todo explotó


# Registramos las rutas y decoradores
init_routes(app)
init_decorators(app)
if __name__ == '__main__':
    # Inicialización de la base de datos
    init_db()
    seed_data()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)