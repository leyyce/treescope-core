from flask import Blueprint, request, jsonify
from services.user_service import create_user, get_user_by_id, get_all_users, update_user, delete_user
from schema.user_schema import user_schema, users_schema

user_blueprint = Blueprint("user_routes", __name__)

@user_blueprint.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400
    user = create_user(username, email)
    return user_schema.jsonify(user), 201

@user_blueprint.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return user_schema.jsonify(user)

@user_blueprint.route("/users", methods=["GET"])
def list_users():
    users = get_all_users()
    return users_schema.jsonify(users)

@user_blueprint.route("/users/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    user = update_user(user_id, username, email)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return user_schema.jsonify(user)

@user_blueprint.route("/users/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    user = delete_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200
