import os
from flask import Flask
from routes.peliculas import peliculas_bp
from database import init_db

app = Flask(__name__)

# Inicializar la base de datos si no existe
init_db()

app.register_blueprint(peliculas_bp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)