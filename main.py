from flask import Flask, render_template, request, redirect, session, url_for
from flask.views import View
from db import DataBaseInteractor

import secrets
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = secrets.token_hex(16)


# Class for flask views
class MyView(View):
    METHODS = ['GET', 'POST']

    def __init__(self, db_address):
        self._db_object = DataBaseInteractor(db_address)
        self.menu = self._db_object.get_from_db('menu', '*')

    # Main page
    def index(self):
        return render_template('index.html', menu=self.menu, title='Home Page')

    # My page redirection
    @staticmethod
    def my_page():
        if 'user_id' not in session:
            return redirect(url_for('enter_profile_get'))
        user_id = session['user_id']
        return redirect(url_for('page', user_id=user_id))

    # Entering profile (GET method) - loads the page
    def enter_profile_get(self):
        return render_template('enter.html', menu=self.menu, title='Login or create page')

    # Entering profile (POST method) - harvest inputted data
    def enter_profile_post(self):
        id_list = self._db_object.get_from_db('users', 'id')
        id_list = [i[0] for i in id_list]

        got_id = int(request.form['id'])
        password = request.form['password']

        if got_id not in id_list:
            return render_template('enter.html', menu=self.menu, title='Login or create page')

        needed_password = self._db_object.get_from_db('users', 'password', id=got_id)[0][0]

        if needed_password != password:
            return render_template('enter.html', menu=self.menu, title='Login or create page')

        session['user_id'] = int(request.form['id'])
        session['password'] = password

        return redirect(url_for('page', user_id=got_id))

    # User page - loads user page
    def page(self, user_id: int):
        needed_password = self._db_object.get_from_db('users', 'password', id=user_id)[0][0]

        if 'password' in session and session['password'] == needed_password:
            user_data = self._db_object.get_from_db('users', '*', id=user_id)
            user_data = user_data[0]
            name = user_data[2]
            last_name = user_data[3]
            age = user_data[5]
            about = user_data[6]
            avatar_name = user_data[7]

            posts = self._db_object.get_from_db('posts', '*', id=user_id)

            return render_template('user_page.html', menu=self.menu, title='User page',
                                   name=name, last_name=last_name, age=age, about=about, user_id=user_id,
                                   avatar_name=avatar_name, posts=posts)

        return redirect(url_for('enter_profile_get'))

    # Create post (GET method) - loads form for adding post
    def create_post_get(self):
        if 'password' in session:
            return render_template('create_post.html', menu=self.menu, title='Create post')
        return redirect(url_for('enter_profile_get'))

    # Create post (POST method) - harvest data from input form
    def create_post_post(self):

        title = request.form['title']
        post_content = request.form['post_content']
        user_id = session['user_id']

        self._db_object.add_post(user_id, title, post_content)
        return redirect(url_for('my_page'))

    # Create page (GET method) - loads creating form
    def create_page_get(self):
        return render_template('create_page.html', menu=self.menu, title='Create your personal page')

    # Create page (POST method) - harvest data from input form
    def create_page_post(self):

        user_id = self._db_object.create_id()
        name = request.form['name']
        last_name = request.form['last_name']
        sex = request.form['sex']
        age = int(request.form['age'])
        about = request.form['about']
        avatar = request.files['avatar']
        avatar_name = avatar.filename
        password = request.form['password']

        if avatar_name[-3:] not in ('png', 'jpg'):
            return render_template('create_page.html', menu=self.menu, title='Create your personal page')

        avatar.save(os.path.join(app.root_path, 'static/avatars', avatar_name))
        self._db_object.add_user(user_id, password, name, last_name, sex, age, about, avatar_name)
        session['user_id'] = user_id
        session['password'] = password

        return redirect(url_for('page', user_id=user_id))

    # Shows existing user pages
    def show_pages(self):
        users = self._db_object.get_from_db('users', '*')
        return render_template('users.html', menu=self.menu, users=users)

    # Routes funcs with url addresses
    def associate_funcs(self):
        app.add_url_rule('/', view_func=self.index, methods=self.METHODS)
        app.add_url_rule('/mypage', view_func=self.my_page, methods=self.METHODS)
        app.add_url_rule('/enter', view_func=self.enter_profile_get, methods=['GET'])
        app.add_url_rule('/enter', view_func=self.enter_profile_post, methods=['POST'])
        app.add_url_rule('/page/<int:user_id>', view_func=self.page, methods=self.METHODS)
        app.add_url_rule('/create', view_func=self.create_page_get, methods=['GET'])
        app.add_url_rule('/create', view_func=self.create_page_post, methods=['POST'])
        app.add_url_rule('/showpages', view_func=self.show_pages, methods=self.METHODS)
        app.add_url_rule('/createpost', view_func=self.create_post_get, methods=['GET'])
        app.add_url_rule('/createpost', view_func=self.create_post_post, methods=['POST'])
