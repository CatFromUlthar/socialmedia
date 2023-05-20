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
                cur.execute("""INSERT INTO menu (title, description) VALUES (?, ?)""",
                            ('Home Page', 'Jump to home page'))
                cur.execute("""INSERT INTO menu (title, description) VALUES (?, ?)""",
                            ('My Page', 'Jump to my page'))
                cur.execute("""INSERT INTO menu (title, description) VALUES (?, ?)""",
                            ('Users', 'List of current site users'))
                cur.execute("""INSERT INTO menu (title, description) VALUES (?, ?)""",
                            ('News', 'Recent info about site'))
                cur.execute("""INSERT INTO menu (title, description) VALUES (?, ?)""",
                            ('About', 'About this site'))

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

    def get_from_db(self, table_name: str, *args) -> list:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            for key in args:
                cur.execute(f"""SELECT {key} FROM {table_name}""")
            result = cur.fetchall()
            return result

    def add_user(self, user_id: int, name: str, last_name: str, sex: str, age: int, about: str) -> None:
        with sqlite3.connect(self._db_name) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO users (id, name, last_name, sex, age, about) \
            VALUES (?, ?, ?, ?, ?, ?)""", (user_id, name, last_name, sex, age, about))

    def create_id(self) -> int:
        raw_list = self.get_from_db('users', 'id')
        id_list = [i[0] for i in raw_list]
        user_id = randint(0, 999999)
        while user_id in id_list:
            user_id = randint(0, 999999)
        return user_id
