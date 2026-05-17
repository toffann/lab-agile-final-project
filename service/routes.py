from flask import jsonify, request, abort
from service.models import Product, Category
from service.common import status
from service import app

# ----------------------------------------------------------------------
# INDEX ROUTE (Opsional - Biar halaman utama tidak 404)
# ----------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    """Root URL response"""
    return jsonify({
        "name": "Product Store REST API",
        "version": "1.0",
        "description": "IBM TDD/BDD Final Project Product Service"
    }), status.HTTP_200_OK

# ----------------------------------------------------------------------
# RETRIEVE A PRODUCT (READ)
# ----------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """Retrieve a single Product based on its ID"""
    app.logger.info("Request to Retrieve a product with id [%s]", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    return jsonify(product.serialize()), status.HTTP_200_OK

# ----------------------------------------------------------------------
# CREATE A NEW PRODUCT
# ----------------------------------------------------------------------
@app.route("/products", methods=["POST"])
def create_products():
    """Creates a Product based on the data in the body"""
    app.logger.info("Request to create a product")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    return jsonify(message), status.HTTP_201_CREATED

# ----------------------------------------------------------------------
# UPDATE AN EXISTING PRODUCT
# ----------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """Update a Product"""
    app.logger.info("Request to Update a product with id [%s]", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK

# ----------------------------------------------------------------------
# DELETE A PRODUCT
# ----------------------------------------------------------------------
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """Delete a Product"""
    app.logger.info("Request to Delete a product with id [%s]", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT

# ----------------------------------------------------------------------
# LIST ALL PRODUCTS & FILTER QUERIES
# ----------------------------------------------------------------------
@app.route("/products", methods=["GET"])
def list_products():
    """Returns all of the Products with filtering options"""
    app.logger.info("Request to list Products...")
    products = []
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        category_value = getattr(Category, category.upper(), None)
        products = Product.find_by_category(category_value)
    elif available:
        available_value = available.lower() in ["true", "1", "yes"]
        products = Product.find_by_availability(available_value)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK