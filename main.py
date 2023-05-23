from flask import Flask, render_template, request, redirect, session, url_for
from flask.views import View
from db import DataBaseInteractor

import secrets

import os
os.chmod('/home/kolovrat/PycharmProjects/socialmedia', 0o777)

app = Flask(__name__, static_url_path='/static')
app.secret_key = secrets.token_hex(16)


class MyView(View):
    methods = ['GET', 'POST']

    def __init__(self, db_address):
        self._db_object = DataBaseInteractor(db_address)
        self.menu = self._db_object.get_from_db('menu', 'title', 'url')

    def index(self):
        return render_template('index.html', menu=self.menu, title='Home Page')

    @staticmethod
    def my_page():
        if 'user_id' not in session:
            return redirect(url_for('enter_profile'))
        user_id = session['user_id']
        return redirect(url_for('page', user_id=user_id))

    def enter_profile(self):
        if request.method == 'GET':
            return render_template('enter.html', menu=self.menu, title='Login or create page')
        elif request.method == 'POST':
            id_list = self._db_object.get_from_db('users', 'id')
            id_list = [i[0] for i in id_list]
            if int(request.form['id']) not in id_list:
                return render_template('enter.html', menu=self.menu, title='Login or create page')
            else:
                session['user_id'] = int(request.form['id'])
                return redirect(url_for('page', user_id=int(request.form['id'])))

    def page(self, user_id: int):
        if ('user_id' in session and user_id != session['user_id']) or 'user_id' not in session:
            return redirect(url_for('enter_profile'))

        else:
            user_data = self._db_object.get_from_db('users', '*', id=user_id)
            user_data = user_data[0]
            name = user_data[1]
            last_name = user_data[2]
            age = user_data[4]
            about = user_data[5]
            avatar_name = user_data[6]

            return render_template('user_page.html', menu=self.menu, title='User page',
                                   name=name, last_name=last_name, age=age, about=about, user_id=user_id,
                                   avatar_name=avatar_name)

    def create_page(self):
        if request.method == 'GET':
            return render_template('create_page.html', menu=self.menu, title='Create your personal page')

        elif request.method == 'POST':

            user_id = self._db_object.create_id()
            name = request.form['name']
            last_name = request.form['last_name']
            sex = request.form['sex']
            age = int(request.form['age'])
            about = request.form['about']
            avatar = request.files['avatar']
            avatar_name = avatar.filename
            if avatar_name[-3:] != 'png' or avatar_name[-3:] != 'jpg':
                return render_template('create_page.html', menu=self.menu, title='Create your personal page')
            avatar.save(os.path.join(app.root_path, '/static/avatars', avatar_name))

            self._db_object.add_user(user_id, name, last_name, sex, age, about, avatar_name)
            session['user_id'] = user_id
            return redirect(url_for('page', user_id=user_id))

    def associate_funcs(self):
        app.add_url_rule('/', view_func=self.index, methods=['GET', 'POST'])
        app.add_url_rule('/mypage', view_func=self.my_page, methods=['GET', 'POST'])
        app.add_url_rule('/enter', view_func=self.enter_profile, methods=['GET', 'POST'])
        app.add_url_rule('/page/<int:user_id>', view_func=self.page, methods=['GET', 'POST'])
        app.add_url_rule('/create', view_func=self.create_page, methods=['GET', 'POST'])


if __name__ == '__main__':
    general_view = MyView('flask.db')
    general_view.associate_funcs()

    app.run(debug=True)
