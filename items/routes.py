import jwt
import sqlalchemy.exc
from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from items.schema import ItemPostSchema, ItemUpdateSchema
from items.model import ItemModel
from db import db
from functools import wraps
from flask import current_app


items_blp = Blueprint('Items', __name__, description='Operations on items')


def check_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        header_token = request.headers.get('Authorization')

        if not header_token:
            return jsonify({'message': 'token not found!'}), 404
        try:
            token = header_token.split(' ')
            decoded_token = jwt.decode(token[1], current_app.config.get('JWT_SECRET_KEY'), ['HS256'])
            return f(*args, **kwargs)
        except Exception:
            return jsonify({'message': 'invalid token key.'})
    return decorator


@items_blp.route('/item')
class Item(MethodView):

    @check_token
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

    @items_blp.response(200, ItemPostSchema)
    def get(self, item_id):
        item = ItemModel.query.get(item_id)
        if not item:
            return jsonify({'message': 'Item not found.'}), 404
        return item

    @check_token
    def delete(self, item_id):
        item = ItemModel.query.get(item_id)
        if not item:
            return jsonify({'message': 'Item not found.'}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted.'}), 200


    @check_token
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

