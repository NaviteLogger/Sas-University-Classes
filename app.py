from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup


def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    # Insert sample users if table is empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        sample_users = [
            ('Alice', 'Smith', 25),
            ('Bob', 'Johnson', 30),
            ('Charlie', 'Brown', 35)
        ]
        cursor.executemany(
            'INSERT INTO users (name, surname, age) VALUES (?, ?, ?)', sample_users)
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def index():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    surname = request.form['surname']
    age = request.form['age']
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (name, surname, age) VALUES (?, ?, ?)', (name, surname, int(age)))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    name = request.form['name']
    surname = request.form['surname']
    age = request.form['age']
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name=?, surname=?, age=? WHERE id=?',
                   (name, surname, int(age), user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    try:
        with open(__file__, 'r') as f:
            code = f.read()
    except Exception as e:
        code = f"Unable to load code: {e}"

    return render_template('about.html', code=code)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
