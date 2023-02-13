import sqlalchemy.exc
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from items.schema import ItemPostSchema, ItemUpdateSchema
from items.model import ItemModel
from db import db
from jwt_token import role_check


items_blp = Blueprint('Items', __name__, description='Operations on items')


@items_blp.route('/item')
class Item(MethodView):

    @role_check('admin')
    @items_blp.arguments(ItemPostSchema)
    def post(self, data):
        try:
            new_item = ItemModel(**data)
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'message': 'Item added.'}), 201
        except sqlalchemy.exc.IntegrityError:
            return jsonify({'message': 'Item already exists in database.'}), 409


@items_blp.route('/item/<int:item_id>')
class ItemId(MethodView):

    @role_check('admin')
    @items_blp.response(200, ItemPostSchema)
    def get(self, item_id):
        item = ItemModel.query.get(item_id)
        if not item:
            return jsonify({'message': 'Item not found.'}), 404
        return item

    @role_check('admin')
    def delete(self, item_id):
        item = ItemModel.query.get(item_id)
        if not item:
            return jsonify({'message': 'Item not found.'}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted.'}), 200

    @role_check('admin')
    @items_blp.arguments(ItemUpdateSchema)
    @items_blp.response(200, ItemPostSchema)
    def put(self, data, item_id):
        item = ItemModel.query.get(item_id)
        if not item:
            return jsonify({'message': 'Item not found.'}), 404
        item.name = data['name']
        item.price = data['price']
        db.session.commit()
        return item
