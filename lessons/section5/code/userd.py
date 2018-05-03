from db import DBContext
from flask_restful import Resource, reqparse


class User(object):
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


class UserRegister(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    user_parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        data = self.user_parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message": "User {} already exists in the database".format(data['username'])}
        
        with DBContext() as c:
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            c.execute(query, (data['username'], data['password']))

        return {"message": "User {} created successfully.".format(data['username'])}, 201
