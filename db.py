import random
import sqlite3
from random import randint


class DataBaseInteractor:

    def __init__(self, db_name: str):
        self._db_name = db_name
        self.ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.create_menu_table()
        self.create_users_table()
        self.create_posts_table()

    def create_menu_table(self) -> None:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS menu (
               title TEXT,
               url TEXT
               )""")

            cur.execute('SELECT COUNT(*) FROM menu')
            res = cur.fetchone()

            if res[0] == 0:
                cur.execute("""INSERT INTO menu VALUES (?, ?)""",
                            ('Home Page', '/'))
                cur.execute("""INSERT INTO menu VALUES (?, ?)""",
                            ('My Page', '/mypage'))
                cur.execute("""INSERT INTO menu VALUES (?, ?)""",
                            ('Users', '/showpages'))
                cur.execute("""INSERT INTO menu VALUES (?, ?)""",
                            ('News', '/'))
                cur.execute("""INSERT INTO menu VALUES (?, ?)""",
                            ('About', '/about'))

    def create_users_table(self) -> None:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
               id INTEGER,
               password TEXT,
               name TEXT,
               last_name TEXT,
               sex TEXT,
               age INTEGER,
               about TEXT,
               avatar_name TEXT
               )""")

    def create_posts_table(self) -> None:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS posts (
               post_id TEXT,
               user_id INTEGER,
               title TEXT,
               post_content TEXT
               )""")

    def get_from_db(self, table_name: str, *columns, **params) -> list:
        with sqlite3.connect(self._db_name) as con:
            result = []
            param_query = ''
            if params is not None:
                for i in params:
                    param_query = f""" WHERE {i} = {(params[i])}"""
            cur = con.cursor()
            for i in columns:
                query = f"""SELECT {i} FROM {table_name}""" + param_query
                cur.execute(query)
                result = result + cur.fetchall()
            return result

    def add_user(self, user_id: int, password: str, name: str, last_name: str, sex: str, age: int,
                 about: str, avatar_name: str) -> None:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO users \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (user_id, password, name, last_name, sex, age, about, avatar_name))

    def add_post(self, post_id: str, user_id: int, title: str, post_content: str) -> None:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO posts \
            VALUES (?, ?, ?, ?)""", (post_id, user_id, title, post_content))

    def create_user_id(self) -> int:
        id_list = self.get_from_db('users', 'id')
        id_list = [i[0] for i in id_list]
        user_id = randint(0, 999999)
        while user_id in id_list:
            user_id = randint(0, 999999)
        return user_id

    def create_post_id(self) -> str:
        post_id = []
        post_list = self.get_from_db('posts', 'post_id')
        post_list = [i[0] for i in post_list]
        for _ in range(5): post_id.append(random.choice(self.ALPHABET))
        while post_id in post_list:
            post_id = []
            for _ in range(5): post_id.append(random.choice(self.ALPHABET))
        post_id = ''.join(post_id)
        return post_id
