from .common import CommonMixin
from db import db


class ItemModel(CommonMixin, db.Model):
    __tablename__ = 'items'

    serial_attrs = ['name', 'price']

    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
