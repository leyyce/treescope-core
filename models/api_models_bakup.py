from flask_restx import fields, Namespace

# Model für die automatische Dokumentation
user_model = user_namespace.model("User", {
    "id": fields.Integer(readOnly=True, description="The unique identifier of a user"),
    "username": fields.String(required=True, description="The user's username"),
    "email": fields.String(required=True, description="The user's email"),
    "roles": fields.String(description="Comma-separated roles for the user")
})
