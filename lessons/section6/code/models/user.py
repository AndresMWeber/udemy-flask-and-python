from db import DBContext


class UserModel(object):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        with DBContext() as c:
            query = "SELECT * FROM users WHERE username=?"
            result = c.execute(query, (username,))
            row = result.fetchone()

            if row and len(row) == 3:
                user = cls(*row)
            else:
                user = None
        return user

    @classmethod
    def find_by_id(cls, _id):
        with DBContext() as c:
            query = "SELECT * FROM users WHERE id=?"
            result = c.execute(query, (_id,))
            row = result.fetchone()

            if row and len(row) == 3:
                user = cls(*row)
            else:
                user = None
        return user