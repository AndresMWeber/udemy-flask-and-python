from db import DBContext
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    price_parser = reqparse.RequestParser()
    price_parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @classmethod
    def delete_by_name(cls, name):
        with DBContext() as c:
            query = "DELETE FROM items WHERE name=?"
            c.execute(query, (name,))

    @classmethod
    def find_by_name(cls, name):
        with DBContext() as c:
            query = "SELECT * FROM items WHERE name=?"
            result = c.execute(query, (name,))
            row = result.fetchone()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, item):
        with DBContext() as c:
            query = "INSERT INTO items VALUES (?, ?)"
            c.execute(query, (item['name'], item['price']))

    @classmethod
    def update(cls, item):
        with DBContext() as c:
            query = "UPDATE items SET price=? WHERE name=?"
            c.execute(query, (item['price'], item['name']))

    @classmethod
    def get(cls, name):
        item = cls.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        item = self.price_parser.parse_args()
        item['name'] = name
        try:
            self.insert(item)
        except:
            return {'message': "An error occurred inserting the item {}.".format(name)}, 400
        return item, 201

    @jwt_required()
    def delete(self, name):
        self.delete_by_name(name)
        return {'message': 'Item %s deleted' % name}

    @jwt_required()
    def put(self, name):
        operation = None
        data = self.price_parser.parse_args()
        data['name'] = name
        existing_item = self.find_by_name(name)
        try:
            if existing_item is None:
                operation = 'inserting'
                self.insert(data)
            else:
                operation = 'updating'
                self.update(data)
        except:
            return {"message": "An error occurred {} the item.".format(operation)}, 500
        return data


class ItemList(Resource):
    @jwt_required()
    def get(self):
        with DBContext() as c:
            query = "SELECT * FROM items"
            result = c.execute(query)
            return {'items': [{'name': row[0], 'price': row[1]} for row in result]}
