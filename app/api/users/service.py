from app.models.user import User
from app.extensions import db

class UserService:
    @staticmethod
    def get_users():
        user_pagination = User.query.paginate(error_out=False)
        resp = {
            'count': len(user_pagination.items),
            'total': user_pagination.total,
            'page': user_pagination.page,
            'per_page': user_pagination.per_page,
            'pages': user_pagination.pages,
            'has_next': user_pagination.has_next,
            'has_prev': user_pagination.has_prev,
            'prev_num': user_pagination.prev_num,
            'next_num': user_pagination.next_num,
            'users': user_pagination.items,
        }
        return resp

    @staticmethod
    def get_user(id_):
        return User.query.get(id_)

    @staticmethod
    def update_user(id, data):
        user = User.query.get(id)
        if not user:
            return f"User with ID {id} does not exist", 404

        username = data['username']

        # Check if the username is taken
        if user.username != username and User.query.filter_by(username=username).first() is not None:
            return 'Username is already taken.', 403

        ## Optional values
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.latitude = latitude
        user.longitude = longitude
        db.session.commit()

        return user, 200

    @staticmethod
    def delete_user(id_):
        user = User.query.get(id_)
        if not user:
            return f"User with ID {id} does not exist", 404

        db.session.delete(user)
        db.session.commit()

        return 'User deleted successfully', 200
