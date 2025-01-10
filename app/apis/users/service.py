from flask import current_app
from app.models.user import User


class UserService:
    @staticmethod
    def get_user(username):
        return User.query.filter_by(username=username).first()
