from flask import Blueprint

from app.models.products import Product


product_bp = Blueprint(__name__, "products")

@product_bp.route("/products", methods=["GET"])
def get_products_list():
    ...


@product_bp.route("/products/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    ...


@product_bp.route("/products", methods=["POST"])
def create_product():
    ...


@product_bp.route("/products", methods=["DELETE"])
def delete_product():
    ...
