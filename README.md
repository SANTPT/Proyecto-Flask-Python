# Movie Tracker

Aplicación web simple desarrollada con Flask para gestionar una colección personal de películas. Permite añadir películas, marcarlas como vistas, calificarlas y eliminarlas.

## Características

- **Gestión de Películas**: Añadir título y género.
- **Estado**: Marcar películas como vistas o pendientes.
- **Calificación**: Asignar una puntuación de 1 a 10.
- **Eliminación**: Borrar películas de la colección.
- **Diseño Minimalista**: Interfaz limpia con tema oscuro.

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd Proyecto-Flask-Python
   ```

2. **Crear y activar un entorno virtual**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecutar la aplicación:
```bash
python app.py
```

Acceder a la aplicación en el navegador en: `http://127.0.0.1:5000`

## Estructura del Proyecto

- `app.py`: Lógica principal de la aplicación Flask.
- `database.py`: Módulo para la gestión de la base de datos SQLite.
- `templates/`: Plantillas Jinja2 para la interfaz de usuario.
- `static/`: Archivos estáticos (CSS).
- `requirements.txt`: Dependencias del proyecto.
- `README.md`: Este archivo.
