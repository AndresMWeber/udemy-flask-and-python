from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
import db
from userd import UserRegister
from item import Item, ItemList


if __name__ == '__main__':
    db.db_init()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'andres'
    api = Api(app=app)

    jwt = JWT(app, authenticate, identity)  # /auth

    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(UserRegister, '/register')

    app.run(port=5000)
