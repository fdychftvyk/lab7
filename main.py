from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Инициализация базы данных
Base = declarative_base()
engine = create_engine("sqlite:///example.db")  # Используем SQLite для простоты
Session = sessionmaker(bind=engine)
session = Session()

# Определение моделей
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    products = relationship("Product", back_populates="category", cascade="all, delete")

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}')"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, category_id={self.category_id})"


# Создание таблиц
Base.metadata.create_all(engine)

# Функции для CRUD-операций
def create_category(name):
    category = Category(name=name)
    session.add(category)
    session.commit()
    print(f"Category '{name}' created with ID={category.id}")
    return category


def create_product(name, price, category_id):
    product = Product(name=name, price=price, category_id=category_id)
    session.add(product)
    session.commit()
    print(f"Product '{name}' created with ID={product.id}")
    return product


def get_products_by_category(category_id):
    products = session.query(Product).filter(Product.category_id == category_id).all()
    for product in products:
        print(product)
    return products


def update_product_category(product_id, new_category_id):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        product.category_id = new_category_id
        session.commit()
        print(f"Product ID={product_id} updated to new category ID={new_category_id}")
    else:
        print(f"Product with ID={product_id} not found")


def delete_category(category_id):
    category = session.query(Category).filter(Category.id == category_id).first()
    if category:
        session.delete(category)
        session.commit()
        print(f"Category ID={category_id} and all associated products deleted")
    else:
        print(f"Category with ID={category_id} not found")


# Пример использования
if __name__ == "__main__":
    # Создание категорий
    electronics = create_category("Electronics")
    groceries = create_category("Groceries")

    # Создание продуктов
    create_product("Laptop", 1200.99, electronics.id)
    create_product("Smartphone", 799.99, electronics.id)
    create_product("Apple", 0.99, groceries.id)

    # Чтение продуктов по категориям
    print("\nProducts in Electronics:")
    get_products_by_category(electronics.id)

    print("\nProducts in Groceries:")
    get_products_by_category(groceries.id)

    # Обновление категории у продукта
    print("\nUpdating product category...")
    update_product_category(1, groceries.id)

    # Удаление категории и связанных продуктов
    print("\nDeleting category...")
    delete_category(electronics.id)

    # Проверка оставшихся продуктов
    print("\nRemaining products:")
    get_products_by_category(groceries.id)