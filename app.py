from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    peliculas = conn.execute('SELECT * FROM peliculas').fetchall()
    conn.close()
    return render_template('index.html', peliculas=peliculas)

@app.route('/add', methods=['POST'])
def add():
    titulo = request.form['titulo']
    genero = request.form['genero']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO peliculas (titulo, genero) VALUES (?, ?)',
        (titulo, genero)
    )
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM peliculas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/watch/<int:id>')
def watch(id):
    conn = get_db_connection()
    conn.execute(
        'UPDATE peliculas SET vista = 1 WHERE id = ?',
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/rate/<int:id>', methods=['POST'])
def rate(id):
    puntuacion = request.form['puntuacion']

    conn = get_db_connection()
    conn.execute(
        'UPDATE peliculas SET puntuacion = ? WHERE id = ?',
        (puntuacion, id)
    )
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)