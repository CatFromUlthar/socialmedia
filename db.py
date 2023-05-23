import sqlite3
from random import randint


class DataBaseInteractor:

    def __init__(self, db_name: str):
        self._db_name = db_name
        self.create_menu_table()
        self.create_users_table()

    def create_menu_table(self) -> None:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS menu (
               title TEXT,
               description TEXT,
               url TEXT
               )""")

            cur.execute('SELECT COUNT(*) FROM menu')
            res = cur.fetchone()

            if res[0] == 0:
                cur.execute("""INSERT INTO menu (title, description, url) VALUES (?, ?, ?)""",
                            ('Home Page', 'Jump to home page', 'http://127.0.0.1:5000'))
                cur.execute("""INSERT INTO menu (title, description, url) VALUES (?, ?, ?)""",
                            ('My Page', 'Jump to my page', 'http://127.0.0.1:5000/mypage'))
                cur.execute("""INSERT INTO menu (title, description, url) VALUES (?, ?, ?)""",
                            ('Users', 'List of current site users', 'http://127.0.0.1:5000'))
                cur.execute("""INSERT INTO menu (title, description, url) VALUES (?, ?, ?)""",
                            ('News', 'Recent info about site', 'http://127.0.0.1:5000'))
                cur.execute("""INSERT INTO menu (title, description, url) VALUES (?, ?, ?)""",
                            ('About', 'About this site', 'http://127.0.0.1:5000'))

    def create_users_table(self) -> None:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
               id INTEGER,
               name TEXT,
               last_name TEXT,
               sex TEXT,
               age INTEGER,
               about TEXT
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

    def add_user(self, user_id: int, name: str, last_name: str, sex: str, age: int, about: str) -> None:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO users (id, name, last_name, sex, age, about) \
            VALUES (?, ?, ?, ?, ?, ?)""", (user_id, name, last_name, sex, age, about))

    def create_id(self) -> int:
        id_list = self.get_from_db('users', 'id')
        user_id = randint(0, 999999)
        while user_id in id_list:
            user_id = randint(0, 999999)
        return user_id
