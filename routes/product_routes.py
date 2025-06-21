from flask import Blueprint, request, jsonify
from models import Product, User, Transaction
from db_config import db
from utils import authenticate_user

bp = Blueprint('product_routes', __name__)

@bp.route('/product', methods=['POST'])
def add_product():
    user = authenticate_user(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    description = data.get("description")

    if not name or not price:
        return jsonify({"error": "Name and price are required"}), 400

    product = Product(name=name, price=price, description=description)
    db.session.add(product)
    db.session.commit()

    return jsonify({"id": product.id, "message": "Product added"}), 201

@bp.route('/product', methods=['GET'])
def list_products():
    products = Product.query.all()
    result = [{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "description": p.description
    } for p in products]
    return jsonify(result), 200

@bp.route('/buy', methods=['POST'])
def buy_product():
    user = authenticate_user(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    product_id = data.get("product_id")
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Invalid product"}), 400

    if user.balance < product.price:
        return jsonify({"error": "Insufficient balance"}), 400

    user.balance -= product.price
    txn = Transaction(user_id=user.id, kind='debit', amt=product.price, updated_bal=user.balance)
    db.session.add(txn)
    db.session.commit()

    return jsonify({"message": "Product purchased", "balance": user.balance}), 200