# Movie Tracker (Flask Edition)

Una aplicación web moderna y minimalista desarrollada con Flask para gestionar y seguir tu colección personal de películas. Este proyecto demuestra una arquitectura limpia separando rutas, servicios y lógica de base de datos.

## Características

- **Gestión Completa (CRUD)**:
  - Añade nuevas películas con título y género.
  - Elimina películas de tu lista fácilmente.
- **Seguimiento de Progreso**:
  - Marca películas como "vistas" con un solo clic.
- **Sistema de Calificación**:
  - Asigna puntuaciones del 1 al 10 a las películas que ya has visto.
- **Interfaz de Usuario**:
  - Diseño responsivo y oscuro optimizado para una excelente experiencia de visualización.
  - Basado en plantillas Jinja2 y CSS puro.

## Tecnologías

- **Backend**: [Flask](https://flask.palletsprojects.com/)
- **Base de Datos**: SQLite3
- **Frontend**: HTML5, CSS3, Jinja2
- **Testing**: Pytest (en desarrollo)

## Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)

## Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd Proyecto-Flask-Python
   ```

2. **Entorno Virtual**:
   ```bash
   # Crear el entorno
   python3 -m venv .venv

   # Activarlo
   source .venv/bin/activate  # En Linux/macOS
   # .venv\Scripts\activate     # En Windows
   ```

3. **Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Base de Datos (Opcional - La app la usa directamente)**:
   Si deseas reiniciar la base de datos con datos de prueba:
   ```bash
   python seed.py
   ```

## Ejecución

Inicia el servidor de desarrollo:
```bash
python app.py
```

La aplicación estará disponible en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Estructura del Proyecto

```text
├── app.py                # Punto de entrada de la aplicación
├── routes/               # Definición de Blueprints y rutas
│   └── peliculas.py      # Rutas relacionadas con películas
├── services/             # Lógica de negocio e interacción DB
│   └── peliculas_service.py
├── templates/            # Plantillas HTML (Jinja2)
├── static/               # Archivos estáticos (CSS/JS)
├── tests/                # Pruebas automatizadas
├── schema.sql            # Definición de la estructura de la DB
├── seed.py               # Script para poblar la DB con datos iniciales
└── requirements.txt      # Dependencias del proyecto
```

## Pruebas

Para ejecutar la suite de pruebas (actualmente en desarrollo):
```bash
pytest
```

---
*Desarrollado como proyecto de aprendizaje para Flask y Python.*
