from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from blocklist import BLOCKLIST
from resources.user import blp as UserBlueprint

# Спочатку ініціалізуємо Flask
app = Flask(__name__)

# Конфігурація для SQLAlchemy та JWT
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"  # SQLite база даних
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "12345"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # Термін дії токену (секунди)

# Ініціалізація компонентів
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Модель користувача
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Модель продукту
class ProductModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id', ondelete='CASCADE'))  # Каскадне видалення
    user = db.relationship('UserModel', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f"<Product {self.name}>"

# Створення всіх таблиць в базі даних
with app.app_context():
    db.create_all()

# Створення користувача
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = UserModel(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully"}), 201

# Отримання користувача за ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserModel.query.get_or_404(user_id)
    return jsonify({"id": user.id, "username": user.username, "password": user.password})

# Оновлення користувача
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = UserModel.query.get_or_404(user_id)
    data = request.get_json()
    
    user.username = data['username']
    user.password = data['password']
    
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# Отримання всіх користувачів
@app.route('/users', methods=['GET'])
def get_users():
    users = UserModel.query.all()
    users_list = [{"id": user.id, "username": user.username, "password": user.password} for user in users]
    return jsonify({"users": users_list})

# Видалення користувача
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UserModel.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# Створення продукту
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    user_id = data.get('user_id')  # Вказуємо користувача, до якого належить продукт
    new_product = ProductModel(
        name=data['name'], 
        brand=data['brand'], 
        price=data['price'], 
        user_id=user_id
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201

# Отримання продукту за ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductModel.query.get_or_404(product_id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "price": product.price
    })

# Оновлення продукту
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = ProductModel.query.get_or_404(product_id)
    data = request.get_json()
    
    product.name = data['name']
    product.brand = data['brand']
    product.price = data['price']
    
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

# Отримання всіх продуктів
@app.route('/products', methods=['GET'])
def get_products():
    products = ProductModel.query.all()
    products_list = [{"id": product.id, "name": product.name, "brand": product.brand, "price": product.price} for product in products]
    return jsonify({"products": products_list})

# Видалення продукту
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = ProductModel.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})

# Запуск додатку
if __name__ == "__main__":
    app.run(debug=True)