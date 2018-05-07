from models.common import CommonMixin
from db import db


class UserModel(CommonMixin, db.Model):
    __tablename__ = 'users'

    serial_attrs = ['username', 'password']

    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
