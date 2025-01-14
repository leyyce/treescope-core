from app.models.user import User


class UserService:
    @staticmethod
    def get_user(id_):
        return User.query.get(id_)
