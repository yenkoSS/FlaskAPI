from flask import request, jsonify, current_app
from functools import wraps
import jwt


def role_check(required_role):
    def token_check(f):
        @wraps(f)
        def decorator(*args, **kwargs):

            header_token = request.headers.get('Authorization')

            if not header_token:
                return jsonify({'message': 'token not found!'}), 404
            try:
                token = header_token.split(' ')
                decoded_token = jwt.decode(token[1], current_app.config.get('JWT_SECRET_KEY'), ['HS256'])
                if decoded_token['role'] == required_role:
                    return f(*args, **kwargs)
                return jsonify({'message': 'You have no access.'}), 403
            except jwt.exceptions.InvalidSignatureError:
                return jsonify({'message': "Invalid token key."}), 401
        return decorator
    return token_check
