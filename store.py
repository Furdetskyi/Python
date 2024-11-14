# models/store.py
from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # Додаємо cascade="all, delete" для каскадного видалення пов'язаних елементів
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")

    # Метод для перетворення об'єкта в словник, щоб легко передавати його як JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            # Додаємо список товарів, пов'язаних з магазином, у вигляді JSON
            "items": [item.to_dict() for item in self.items]
        }