from .common import CommonMixin
from db import db


class StoreModel(CommonMixin, db.Model):
    __tablename__ = 'stores'

    serial_attrs = ['name']

    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        json_repr = super(StoreModel, self).json()
        json_repr['items'] = [item.json() for item in self.items.all()]
        return json_repr
