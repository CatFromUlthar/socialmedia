from flask import Flask, render_template, request, redirect, session, url_for
from db import DataBaseInteractor

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/', methods=['GET'])
def main_page():
    my_db = DataBaseInteractor('flask.db')
    menu = my_db.get_from_db('menu', 'title')
    return render_template('index.html', menu=menu, title='Home Page')


@app.route('/mypage', methods=['GET'])
def my_page():
    if 'id' not in session:
        return redirect('/login')
    else:
        return redirect(url_for('show_page', user_id=session['id']))


@app.route('/login', methods=['GET'])
def login_get():
    my_db = DataBaseInteractor('flask.db')
    menu = my_db.get_from_db('menu', 'title')
    if 'id' not in session:
        return render_template('login.html', menu=menu, title='Login')


@app.route('/login', methods=['POST'])
def login_post():
    my_db = DataBaseInteractor('flask.db')

    user_id = my_db.create_id()

    name = request.form['name']
    last_name = request.form['last_name']
    sex = request.form['sex']
    age = int(request.form['age'])
    about = request.form['about']

    my_db.add_user(user_id, name, last_name, sex, age, about)
    session['id'] = user_id
    return redirect(url_for('show_page', user_id=user_id))


@app.route('/page/<int:user_id>', methods=['GET'])
def show_page(user_id):
    my_db = DataBaseInteractor('flask.db')
    user_list = my_db.get_from_db_with_params('users', 'id', str(user_id), 'name', '*')

    name = user_list[0][1]
    last_name = user_list[0][2]
    age = user_list[0][4]
    about = user_list[0][5]

    return render_template('user_page.html', name=name, last_name=last_name, age=age, about=about)


if __name__ == '__main__':
    app.run(debug=True)
