from db import DBContext
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    user_parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    def post(self):
        data = self.user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "User {} already exists in the database".format(data['username'])}
        
        with DBContext() as c:
            query = "INSERT INTO users VALUES (NULL, ?, ?)"
            c.execute(query, (data['username'], data['password']))

        return {"message": "User {} created successfully.".format(data['username'])}, 201
