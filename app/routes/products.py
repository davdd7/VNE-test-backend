from flask import Blueprint, jsonify, request
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from app.models.products import db, Product, Category, ProductSize, Size


product_bp = Blueprint("products", __name__)

@product_bp.route("/products", methods=["GET"])
def get_products_list():
    category_name = request.args.get("category")
    product_name = request.args.get("name")

    stmt = select(Product).join(Product.category)

    if product_name:
        stmt = stmt.where(func.lower(Product.name).contains(func.lower(product_name)))

    if category_name:
        stmt = stmt.where(func.lower(Category.name).contains(func.lower(category_name)))

    products = db.session.scalars(stmt).all()

    res_list = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "category": product.category.name
        } for product in products
    ]

    return jsonify(
        {
            "status": True,
            "result": res_list
        }
    )


@product_bp.route("/products/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    stmt = (
        select(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.size_associations).joinedload(ProductSize.size_ref)
        )
        .where(Product.id == product_id)
    )

    product = db.session.scalar(stmt)

    if not product:
        return jsonify(
            {
                "error": "No product with id {}".format(product_id)
            }
        )

    res_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category.name,
        "sizes": [
            {
                "name": assoc.size_ref.name,
                "quantity": assoc.quantity
            }
            for assoc in product.size_associations
        ]
    }

    return jsonify(
        {
            "status": True,
            "result": res_data
        }
    )


@product_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()

    name = data.get("name")
    price = data.get("price")
    description = data.get("description")

    if not name or not price:
        return jsonify(
            {
                "error": "name and price are required!"
            }
        )

    category_name = data.get("category_name")
    if category_name:
        category = db.session.scalar(
            select(Category).where(func.lower(Category.name) == func.lower(category_name))
        )

        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.flush()

    else:
        return jsonify(
            {
                "error": "no category"
            }
        )

    product = Product(
        name=name, description=description,
        price=price, category_id=category.id
    )
    db.session.add(product)
    db.session.flush()

    for size_data in data.get("sizes", []):
        size = db.session.scalar(
            select(Size).where(func.lower(Size.name) == func.lower(size_data)["size_name"])
        )
        if not size:
            size = Size(name=size_data["size_name"])
            db.session.add(size)
            db.session.flush()

        product_size = ProductSize(
            product_id=product.id,
            size_id=size.id,
            quantity=size_data.get("quantity", 0)
        )

        db.session.add(product_size)

    db.session.commit()

    return jsonify(
        {
            "result": True
        }
    )


@product_bp.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = db.session.get(Product, product_id)

    if not product:
        return jsonify(
            {
                "error": "no product with this key"
            }
        )

    db.session.delete(product)
    db.session.commit()

    return jsonify(
        {
            "status": True
        }
    )
