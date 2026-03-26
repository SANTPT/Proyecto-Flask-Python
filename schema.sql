CREATE TABLE peliculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    genero TEXT,
    vista INTEGER DEFAULT 0,
    puntuacion INTEGER
);