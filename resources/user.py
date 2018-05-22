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

        UserModel(**data).save_to_db()

        return {"message": "User {} created successfully.".format(data['username'])}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200
