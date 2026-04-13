import os
from flask import Flask
from routes.peliculas import init_routes
from database import init_db
from seed import seed_data

app = Flask(__name__)

# Registramos las rutas directamente en la app sin Blueprints
init_routes(app)

if __name__ == '__main__':
    # Inicialización de la base de datos
    init_db()
    seed_data()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)