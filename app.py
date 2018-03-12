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

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db
#
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

Articles = Articles()

# Page Routing

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

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
        connection = sqlite3.connect('myflaskapp.db')
        cur = connection.cursor()

        cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', (record, name, username, email, password, register_date))
        connection.commit()
        connection.close()

        flash('You are now registered and can log in.', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
