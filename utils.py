from flask import request
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    return generate_password_hash(password)

def verify_password(plain_password, hashed_password):
    return check_password_hash(hashed_password, plain_password)

def authenticate_user(req):
    auth = req.authorization
    if not auth:
        return None
    user = User.query.filter_by(username=auth.username).first()
    if user and verify_password(auth.password, user.password):
        return user
    return None