from db import db


class CommonMixin(object):
    serial_attrs = []
    id = db.Column(db.Integer, primary_key=True)

    def json(self):
        return {attr: getattr(self, attr) for attr in self.serial_attrs}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()
