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
def view_courses():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM Courses').fetchall()
    conn.close()
    return render_template('view_courses.html', courses = courses)

@app.route('/add', methods = ('GET', 'POST'))
def add_course():
    if request.method == 'POST':
        title = request.form['title']
        teacher = request.form['teacher']
        start_month = request.form['start_month']

        if not title or not teacher or not start_month:
            flash('All fields are required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO courses (title, teacher, start_month) VALUES (?, ?, ?)', (title, teacher, start_month)) 

        conn.commit()
        conn.close()
        return redirect (url_for('view_courses'))

    return render_template('add_course.html')

@app.route('/edit/<int:id>', methods = ('GET', 'POST'))
def edit_course(id):
    conn = get_db_connection()
    course = conn.execute('SELECT * FROM course WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        teacher = request.form['teacher']
        start_month = request.form['start_month']

        if not title or not teacher or not start_month:
            flash('All fields are required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE courses SET title = ?, teacher = ?, start_month = ?,  WHERE id = ?', (title, teacher, start_month, id)) 

            conn.commit()
            conn.close()
            return redirect (url_for('view_courses')) 

    return render_template('edit_course.html', course = course)

@app.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete_course(id):
    conn = get_db_connection()
    course = conn.execute('SELECT * FROM course WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        conn.execute('DELETE FROM course WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('view_course'))

    return render_template('delete_course.html', course=course)



if __name__ == '__main__':
    app.run(debug=True)




