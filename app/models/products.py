from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category", back_populates="products")

    size_associations = db.relationship("ProductSize",
                                        back_populates="product_ref",
                                        cascade="all, delete-orphan")


class Size(db.Model):
    __tablename__ = "sizes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))

    product_associations = db.relationship("ProductSize", back_populates="size_ref")


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))

    products = db.relationship("Product", back_populates="category")


class ProductSize(db.Model):
    __tablename__ = "product_sizes"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    size_id = db.Column(db.Integer, db.ForeignKey("sizes.id"), primary_key=True)

    quantity = db.Column(db.Integer, default=0)

    product_ref = db.relationship("Product", back_populates="size_associations")
    size_ref = db.relationship("Size", back_populates="product_associations")
