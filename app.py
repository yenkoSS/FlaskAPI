from flask import Flask
from db import db
from stores.routes import stores_blp
from items.routes import items_blp


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['JWT_SECRET_KEY'] = 'strongestpasswordever'

    app.register_blueprint(stores_blp)
    app.register_blueprint(items_blp)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)


if __name__ == '__main__':
    create_app()
