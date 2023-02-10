from db import db

class StoreModel(db.Model):

    __tablename__ = 'Store'
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    name = db.Column(db.String(), unique=True)

