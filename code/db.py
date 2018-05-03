import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DBContext(object):
    """
    Simple CM for sqlite3 databases. Commits everything at exit.
    """
    DEFAULT_DB = 'data.db'

    def __init__(self, path=None):
        self.path = path or self.DEFAULT_DB
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


def db_init():
    with DBContext() as c:
        create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
        c.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
        c.execute(create_table)
