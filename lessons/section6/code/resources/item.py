from db import DBContext
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    price_parser = reqparse.RequestParser()
    price_parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @classmethod
    def get(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        data = self.price_parser.parse_args()
        try:
            item = ItemModel(name, data['price']).insert()
        except:
            return {'message': "An error occurred inserting the item {}.".format(name)}, 400
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        ItemModel.delete_by_name(name)
        return {'message': 'Item %s deleted' % name}

    @jwt_required()
    def put(self, name):
        operation = None

        existing_item = ItemModel.find_by_name(name)
        data = self.price_parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            if existing_item is None:
                operation = 'inserting'
                item.insert()
            else:
                operation = 'updating'
                item.update()
        except:
            return {"message": "An error occurred {} the item.".format(operation)}, 500
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        with DBContext() as c:
            query = "SELECT * FROM items"
            result = c.execute(query)
            return {'items': [ItemModel(*row).json() for row in result]}
