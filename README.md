# 💰 Wallet API 
This project is a simple Flask-based REST API for user authentication and wallet operations. It includes features like user registration, login with password hashing, and database integration with MySQL.
---

## 🚀 Features

🔐 Secure password hashing (Werkzeug)
- 🛢️ MySQL database with SQLAlchemy ORM
- 📦 Flask Blueprints for modular code
- ☁️ Ready-to-deploy on Render

The API provides the following functionalities:
- ✅ Register User (POST /register)
- ✅ Fund Account (POST /fund)
- ✅ Pay Another User (POST /pay)
- ✅ Check Balance (GET /bal) - with optional currency conversion.
- ✅ View Transaction History (GET /stmt)
- ✅ Add Product (POST /product)
- ✅ List All Products (GET /product)
- ✅ Buy a Product (POST /buy)
- ✅ User Login (`/login`)

---

## 🛠️ Tech Stack

- **Framework:** Flask (Python)
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Deployment:** Render
- **Other Tools:** Git, GitHub, Dotenv

---

## 📦 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Arpitadash02/wallet-api.git
cd wallet-api
```
### 2. Set up virtual environment
```bash
python -m venv env
env\Scripts\activate  # On Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```

✅ Start Command
```bash
python app.py
```
