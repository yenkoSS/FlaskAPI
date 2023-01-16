from flask import Response
import sqlalchemy.exc
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from stores.schema import CreateStoreSchema, UpdateStoreSchema
from stores.model import StoreModel
from db import db


stores_blp = Blueprint('Stores', __name__, description='Operations on stores')

@stores_blp.route('/store')
class Store(MethodView):

    @stores_blp.arguments(CreateStoreSchema)
    @stores_blp.response(201, CreateStoreSchema)
    def post(self, data):
        new_store = StoreModel(**data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            abort(500, message="Store already exists.")
        return new_store


@stores_blp.route('/store/<int:store_id>')
class StoreId(MethodView):

    @stores_blp.response(200, CreateStoreSchema)
    def get(self, store_id):
        store = StoreModel.query.filter(StoreModel.id == store_id).first()
        if store:
            return store
        else:
            return abort(404, exc='Hello World')

    @stores_blp.arguments(UpdateStoreSchema)
    @stores_blp.response(200, CreateStoreSchema)
    def put(self, data, store_id):

        store = StoreModel.query.filter(StoreModel.id == store_id).first()
        if store:
            store.name = data['name']
            try:
                db.session.commit()
            except Exception:
                abort(500, message='Store name already exists.')
            return store
        else:
            abort(404, message="Store not found.")


    def delete(self, store_id):
        store = StoreModel.query.filter(StoreModel.id == store_id).first()
        if store:
            try:
                db.session.delete(store)
                db.session.commit()
                return {'message': 'Store deleted.'}
            except sqlalchemy.exc.IntegrityError:
                abort(500, message='Store not found.')
        return {'message': 'Store not found.'}, 404