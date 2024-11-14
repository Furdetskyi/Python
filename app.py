# app.py
from flask import Flask, jsonify
from flask_smorest import Api
from db import db
import models
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from models.store import StoreModel

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["OPENAPI_VERSION"] = "3.0.3"  # Додаємо версію OpenAPI
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

@app.route("/")
def home():
    # Отримуємо всі магазини з бази даних
    stores = StoreModel.query.all()
    
    # Перетворюємо кожен магазин на словник за допомогою методу to_dict
    return {"stores": [store.to_dict() for store in stores]}

    return app

# Додано для запуску додатку
if __name__ == "__main__":
    app = create_app()  # Створюємо додаток
    app.run(debug=True)  # Запускаємо сервер Flask в режимі налагодження