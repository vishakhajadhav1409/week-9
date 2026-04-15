from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user = User(username=data["username"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)

    return jsonify({"msg": "Invalid credentials"}), 401