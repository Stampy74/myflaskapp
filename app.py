from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
import sqlite3
import datetime
from flask import g
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config SQLITE 3
DATABASE = 'myflaskapp.db'
Articles = Articles()

# Page Routing

# Home Page
@app.route('/')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# All Articles
@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

# Single Article
@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)

# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        record = None # Can leave this field out of database. Rowid autoassigned
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        register_date = datetime.datetime.now()
        #register_date = None

        #Create Connection & Cursor
        connection = sqlite3.connect(DATABASE)
        cur = connection.cursor()

        cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', (record, name, username, email, password, register_date))
        connection.commit()
        connection.close()

        flash('You are now registered and can log in.', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        connection = sqlite3.connect(DATABASE)
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()

        # Get user by username

        result = cur.execute("SELECT * FROM users WHERE username = ?", (username, ))
        # Get stored hash
        password_test = result.fetchone()

        # Determine if a result was returned
        if password_test != None:

            password = password_test['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                #app.logger.info('Password Matched')
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in.', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)
            # Close connection
            connection.close()
        else:
            error = 'Username not found'
            return  render_template('login.html', error=error)

        connection.close()

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out.', 'success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
