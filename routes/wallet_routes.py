from flask import Blueprint, request, jsonify
from models import User, Transaction
from db_config import db
from utils import authenticate_user
import requests
import os

bp = Blueprint('wallet_routes', __name__)

@bp.route('/fund', methods=['POST'])
def fund():
    user = authenticate_user(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    amt = float(data.get("amt", 0))
    if amt <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    user.balance += amt
    txn = Transaction(user_id=user.id, kind='credit', amt=amt, updated_bal=user.balance)
    db.session.add(txn)
    db.session.commit()

    return jsonify({"balance": user.balance}), 200

@bp.route('/pay', methods=['POST'])
def pay():
    user = authenticate_user(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    recipient = User.query.filter_by(username=data.get("to")).first()
    amt = float(data.get("amt", 0))

    if not recipient:
        return jsonify({"error": "Recipient not found"}), 400
    if amt <= 0 or user.balance < amt:
        return jsonify({"error": "Insufficient balance or invalid amount"}), 400

    user.balance -= amt
    recipient.balance += amt

    db.session.add(Transaction(user_id=user.id, kind='debit', amt=amt, updated_bal=user.balance))
    db.session.add(Transaction(user_id=recipient.id, kind='credit', amt=amt, updated_bal=recipient.balance))
    db.session.commit()

    return jsonify({"balance": user.balance}), 200

@bp.route('/bal', methods=['GET'])
def balance():
    user = authenticate_user(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    currency = request.args.get("currency")
    balance = user.balance

    if currency and currency.upper() != "INR":
        res = requests.get(f"https://api.currencyapi.com/v3/latest?apikey={os.getenv('CURRENCY_API_KEY')}&currencies={currency}&base_currency=INR")
        rate = res.json().get("data", {}).get(currency.upper(), {}).get("value")
        if not rate:
            return jsonify({"error": "Conversion rate not available"}), 400
        return jsonify({"balance": round(balance * rate, 2), "currency": currency.upper()}), 200

    return jsonify({"balance": balance, "currency": "INR"}), 200

@bp.route('/stmt', methods=['GET'])
def stmt():
    user = authenticate_user(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    txns = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).all()
    result = [
        {"kind": t.kind, "amt": t.amt, "updated_bal": t.updated_bal, "timestamp": t.timestamp.isoformat()} for t in txns
    ]
    return jsonify(result), 200