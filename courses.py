from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

app.secret_key =  "supersecretkey"

def get_db_connection():
    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses')
def view_games():
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return render_template('view_courses.html', games = games)

@app.route('/add', methods = ('GET', 'POST'))
def add_courses():
    if request.method == 'POST':
        title = request.form['title']
        platform = request.form['platform']
        genre = request.form['genre']
        year = request.form['year']
        sales = request.form['sales']

        if not title or not platform or not year or not sales:
            flash('All fields are required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO games (title, platform, genre, year, sales) VALUES (?, ?, ?, ?, ?)', (title, platform, genre, year, sales)) 

        conn.commit()
        conn.close()
        return redirect (url_for('view_games'))

    return render_template('add_game.html')

@app.route('/edit/<int:id>', methods = ('GET', 'POST'))
def edit_game(id):
    conn = get_db_connection()
    game = conn.execute('SELECT * FROM games WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        platform = request.form['platform']
        genre = request.form['genre']
        year = request.form['year']
        sales = request.form['sales']

        if not title or not platform or not year or not sales:
            flash('All fields are required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE games SET title = ?, platform = ?, genre = ?, year = ?, sales = ? WHERE id = ?', (title, platform, genre, year, sales, id)) 

            conn.commit()
            conn.close()
            return redirect (url_for('view_games')) 

    return render_template('edit_game.html', game = game)

@app.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete_game(id):
    conn = get_db_connection()
    game = conn.execute('SELECT * FROM games WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        conn.execute('DELETE FROM games WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('view_games'))

    return render_template('delete_game.html', game=game)




if __name__ == '__main__':
    app.run(debug=True)




