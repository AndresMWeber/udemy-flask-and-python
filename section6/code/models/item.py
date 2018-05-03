from db import DBContext


class ItemModel(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

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
            return cls(*row)

    def insert(self):
        with DBContext() as c:
            query = "INSERT INTO items VALUES (?, ?)"
            c.execute(query, (self.name, self.price))

    def update(self):
        with DBContext() as c:
            query = "UPDATE items SET price=? WHERE name=?"
            c.execute(query, (self.price, self.name))
