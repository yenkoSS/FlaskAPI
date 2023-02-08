import jwt
from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from items.schema import ItemPostSchema, ItemUpdateSchema
from items.model import ItemModel
from db import db
from functools import wraps


item_blp = Blueprint('Items', __name__, description='Operations on items')


def check_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        header_token = request.headers.get('Authorization')

        if not header_token:
            return jsonify({'message': 'token not found!'}), 404
        try:
            token = header_token[7::]
            decoded_token = jwt.decode(token, 'strongestpasswordever', ['HS256'])
            return f(*args, **kwargs)
        except Exception:
            return jsonify({'message': 'invalid token key.'})
    return decorator


@item_blp.route('/item')
class Item(MethodView):

    @check_token
    @item_blp.arguments(ItemPostSchema)
    def post(self, data):
        item = ItemModel.query.filter(data['name'] == ItemModel.name).first()
        if not item:
            new_item = ItemModel(**data)
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'message': 'Item added.'}), 201
        return jsonify({'message': 'Item already exists in database.'}), 409


@item_blp.route('/item/<int:item_id>')
class ItemId(MethodView):

    @check_token
    @item_blp.response(200, ItemPostSchema)
    def get(self, item_id):
        item = ItemModel.query.filter(ItemModel.id == item_id).first()
        if item:
            return item
        return jsonify({'message': 'Item not found.'}), 404

    @check_token
    def delete(self, item_id):
        item = ItemModel.query.filter(ItemModel.id == item_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Item deleted.'}), 200
        return jsonify({'message': 'Item not found.'}), 404

    @check_token
    @item_blp.arguments(ItemUpdateSchema)
    @item_blp.response(200, ItemPostSchema)
    def put(self, data, item_id):
        item = ItemModel.query.filter(ItemModel.id == item_id).first()
        if item:
            item.name = data['name']
            item.price = data['price']
            db.session.commit()
            return item
        return jsonify({'message': 'Item not found.'}), 404
