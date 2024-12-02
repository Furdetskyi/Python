import time
from app import db, UserModel, ProductModel

def measure_time(func):
    """Декоратор для вимірювання часу виконання функції"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        return elapsed_time, result
    return wrapper

@measure_time
def insert_data(n):
    """Масове вставлення даних"""
    for i in range(n):
        product = ProductModel(name=f"Product{i}", brand=f"Brand{i}", price=i)
        db.session.add(product)
    db.session.commit()

@measure_time
def select_data():
    """Вибірка даних"""
    products = ProductModel.query.all()
    return len(products)

@measure_time
def update_data():
    """Оновлення даних"""
    products = ProductModel.query.all()
    for product in products:
        product.price += 1
    db.session.commit()

@measure_time
def delete_data():
    """Видалення даних"""
    products = ProductModel.query.all()
    for product in products:
        db.session.delete(product)
    db.session.commit()

def benchmark():
    results = []
    for n in [1000, 10000, 100000, 1000000]:
        print(f"Виконання операцій для {n} записів:")
        
        # Insert
        elapsed_time, _ = insert_data(n)
        print(f"INSERT: {elapsed_time:.2f} сек.")
        results.append({"operation": "INSERT", "records": n, "time": elapsed_time})

        # Select
        elapsed_time, count = select_data()
        print(f"SELECT: {elapsed_time:.2f} сек. (Кількість записів: {count})")
        results.append({"operation": "SELECT", "records": n, "time": elapsed_time})

        # Update
        elapsed_time, _ = update_data()
        print(f"UPDATE: {elapsed_time:.2f} сек.")
        results.append({"operation": "UPDATE", "records": n, "time": elapsed_time})

        # Delete
        elapsed_time, _ = delete_data()
        print(f"DELETE: {elapsed_time:.2f} сек.")
        results.append({"operation": "DELETE", "records": n, "time": elapsed_time})

    return results

if __name__ == "__main__":
    with db.app.app_context():  # Використовуйте контекст додатку
        results = benchmark()
        print("\nПорівняльна таблиця:")
        for res in results:
            print(res)
