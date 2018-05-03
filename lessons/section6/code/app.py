from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.register import UserRegister
from resources.item import Item, ItemList
from db import db

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'andres'
    api = Api(app=app)
    db(app)

    jwt = JWT(app, authenticate, identity)  # /auth

    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(UserRegister, '/register')

    app.run(port=5000)
