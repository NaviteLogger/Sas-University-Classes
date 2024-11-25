from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management


@app.route('/')
def home():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
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


@app.route('/summary', methods=['GET'])
def summary():
    form_data = session.get('form_data', {})
    return render_template('summary.html', form_data=form_data)


@app.route('/logout')
def logout():
    session.pop('form_data', None)
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(debug=True)
