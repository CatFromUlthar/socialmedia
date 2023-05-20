from flask import Flask, render_template, request, flash, redirect
from db import DataBaseInteractor

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/', methods=['GET'])
def main_page():
    my_db = DataBaseInteractor('flask.db')
    menu = my_db.get_from_db('menu', 'title')
    return render_template('index.html', menu=menu, title='Home Page')


if __name__ == '__main__':
    app.run(debug=True)
