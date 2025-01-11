from flask import request, jsonify
from flask_praetorian import auth_required, roles_required
from flask_restx import Namespace, Resource
from config.auth import guard
from models.restx_documentation import create_restx_model
from models.user import User
from services.user_service import create_user, get_all_users

# Namespace für die User-API
user_namespace = Namespace("User", description="User-related operations")

user_doc_model = user_namespace.model("User", create_restx_model(User, user_namespace))

@user_namespace.route("/register")
class UserRegister(Resource):
    @user_namespace.expect(user_doc_model)
    @user_namespace.response(201, "User created")
    @user_namespace.response(400, "Validation Error")
    def post(self):
        """Register a new user."""
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if not username or not email or not password:
            return jsonify({"error": "All fields are required"}), 400
        user = create_user(username, email, password)
        return jsonify({"message": "User created"}), 201

@user_namespace.route("/login")
class UserLogin(Resource):
    @user_namespace.response(200, "Login successful")
    @user_namespace.response(401, "Unauthorized")
    def post(self):
        """Login and retrieve a token."""
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = guard.authenticate(username, guard.hash_password(password))
        return jsonify({"access_token": guard.encode_jwt_token(user)})

@user_namespace.route("/")
class UserList(Resource):
    @auth_required
    @roles_required("admin")
    @user_namespace.marshal_with(user_doc_model, as_list=True)
    def get(self):
        """Retrieve all users (admin only)."""
        users = get_all_users()
        return users
