from flask import Flask, request
from db import db
from models import StoreModel, ItemModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'  # Підключення до SQLite
db.init_app(app)

# Створення магазину
@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = StoreModel(name=request_data["name"])  # Створення нового магазину
    db.session.add(new_store)  # Додавання магазину до сесії
    db.session.commit()  # Застосування змін і збереження в базі даних
    return {"id": new_store.id, "name": new_store.name}, 201

# Створення товару для магазину
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    store = StoreModel.query.filter_by(name=name).first()  # Пошук магазину за ім'ям
    if store:
        new_item = ItemModel(name=request_data["name"], price=request_data["price"], store_id=store.id)
        db.session.add(new_item)  # Додавання товару до сесії
        db.session.commit()  # Збереження товару в базі
        return {"id": new_item.id, "name": new_item.name, "price": new_item.price}, 201
    return {"message": "Store not found"}, 404

# Отримання магазину за ID
@app.get("/store/<int:store_id>")
def get_store(store_id):
    store = StoreModel.query.get(store_id)  # Отримання магазину за ID
    if not store:
        return {"message": "Store not found"}, 404
    return {"id": store.id, "name": store.name, "items": [{"id": item.id, "name": item.name, "price": item.price} for item in store.items]}

# Оновлення магазину
@app.put("/store/<int:store_id>")
def update_store(store_id):
    request_data = request.get_json()
    store = StoreModel.query.get(store_id)  # Отримання магазину
    if store:
        store.name = request_data["name"]  # Оновлення атрибуту
        db.session.commit()  # Збереження змін
        return {"id": store.id, "name": store.name}
    return {"message": "Store not found"}, 404

# Отримання всіх магазинів
@app.get("/stores")
def get_all_stores():
    stores = StoreModel.query.all()  # Отримуємо всі магазини з бази даних
    return {
        "stores": [
            {
                "name": store.name,
                "items": [
                    {
                        "name": item.name,
                        "price": item.price
                    } for item in store.items  # Це повинно повернути всі товари магазину
                ]
            } for store in stores
        ]
    }

# Видалення магазину
@app.delete("/store/<int:store_id>")
def delete_store(store_id):
    store = StoreModel.query.get(store_id)  # Отримання магазину
    if store:
        db.session.delete(store)  # Видалення магазину
        db.session.commit()  # Застосування змін
        return {"message": "Store deleted"}
    return {"message": "Store not found"}, 404

# Видалення товару
@app.delete("/store/<int:store_id>/item/<int:item_id>")
def delete_item(store_id, item_id):
    store = StoreModel.query.get(store_id)
    if store:
        item = ItemModel.query.get(item_id)
        if item and item.store_id == store.id:
            db.session.delete(item)  # Видалення товару
            db.session.commit()  # Застосування змін
            return {"message": "Item deleted"}
        return {"message": "Item not found"}, 404
    return {"message": "Store not found"}, 404

if __name__ == "__main__":
    app.run(debug=True)