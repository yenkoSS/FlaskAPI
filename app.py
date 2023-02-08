from flask import Flask
from db import db
from stores.routes import stores_blp
from items.routes import item_blp


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    app.register_blueprint(stores_blp)
    app.register_blueprint(item_blp)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)


if __name__ == '__main__':
    create_app()
