import sqlalchemy.exc
from flask_smorest import Blueprint
from flask.views import MethodView
from stores.schema import StorePostSchema, StoreUpdateSchema
from stores.model import StoreModel
from flask import jsonify
from db import db
from JWT.jwt_token import role_check
from JWT.roles import ADMIN, MODERATOR, BASIC


stores_blp = Blueprint('Stores', __name__, description='Operations on stores')

@stores_blp.route('/store')
class Store(MethodView):

    @role_check([ADMIN, MODERATOR])
    @stores_blp.arguments(StorePostSchema)
    def post(self, data):
        try:
            new_store = StoreModel(**data)
            db.session.add(new_store)
            db.session.commit()
            return jsonify({'message': 'Store added.'}), 201
        except sqlalchemy.exc.IntegrityError:
            return jsonify({'message': 'Store already exists in database.'}), 409



@stores_blp.route('/store/<int:store_id>')
class ItemId(MethodView):

    @role_check([ADMIN, MODERATOR, BASIC])
    @stores_blp.response(200, StorePostSchema)
    def get(self, store_id):
        store = StoreModel.query.get(store_id)
        if not store:
            return jsonify({'message': 'Store not found.'}), 404
        return store

    @role_check([ADMIN])
    def delete(self, store_id):
        store = StoreModel.query.get(store_id)
        if not store:
            return jsonify({'message': 'Store not found.'}), 404
        db.session.delete(store)
        db.session.commit()
        return jsonify({'message': 'Store deleted.'}), 200

    @role_check([ADMIN])
    @stores_blp.arguments(StoreUpdateSchema)
    @stores_blp.response(200, StorePostSchema)
    def put(self, data, store_id):
        store = StoreModel.query.get(store_id)
        if not store:
            return jsonify({'message': 'Store not found.'}), 404
        store.name = data['name']
        store.price = data['price']
        db.session.commit()
        return store
