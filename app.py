from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

# Hardcoded credentials
USERNAME = 'username'
PASSWORD = 'password'


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    endpoints = [
        {'path': '/', 'description': 'Home'},
        {'path': '/login', 'description': 'Logowanie'},
        {'path': '/register', 'description': 'Rejestracja'},
        {'path': '/summary', 'description': 'Podsumowanie'},
        {'path': '/about', 'description': 'Plik app.py'},
        {'path': '/logout', 'description': 'Wylogowanie'},
    ]

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('register'))
        else:
            return render_template('login.html', error='Invalid username or password', endpoints=endpoints)

    return render_template('login.html', endpoints=endpoints)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Collect form data
        form_data = {
            'name': request.form.get('name'),
            'surname': request.form.get('surname'),
            'address': request.form.get('address'),
            'housing': request.form.get('housing'),
            'phone': request.form.get('phone'),
            'dob': request.form.get('dob'),
            'license': request.form.get('license'),
            'password': request.form.get('password'),
            'gender': request.form.get('gender'),
            'city': request.form.get('city'),
            'country': request.form.get('country'),
        }
        # Store data temporarily in session
        session['form_data'] = form_data
        return redirect(url_for('summary'))

    return render_template('register.html')


@app.route('/about')
def about():
    try:
        with open(__file__, 'r') as f:
            code = f.read()
    except Exception as e:
        code = f"Unable to load code: {e}"

    return render_template('about.html', code=code)


@app.route('/summary', methods=['GET'])
def summary():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    form_data = session.get('form_data', {})
    return render_template('summary.html', form_data=form_data)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('form_data', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
