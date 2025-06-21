from flask import Flask, jsonify
from models import db
from routes import auth_routes, wallet_routes, product_routes
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Wallet API is running!"})

app.register_blueprint(auth_routes)
app.register_blueprint(wallet_routes)
app.register_blueprint(product_routes)

if __name__ == "__main__":
    app.run(debug=True)