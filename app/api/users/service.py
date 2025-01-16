from app.models.user import User
from app.extensions import db, guard

class UserService:
    @staticmethod
    def get_user(id_):
        return User.query.get(id_)

    @staticmethod
    def update_user(data, id):
        user = User.query.get(id)
        if not user:
            return 404, {'message': 'User not found'}
        try:
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            user.username = username if username is not None else user.username
            user.first_name = first_name if first_name is not None else user.first_name
            user.last_name = last_name if last_name is not None else user.last_name
            user.email = email if email is not None else user.email
            user.hashed_password = guard.hash_password(password) if password is not None else user.hashed_password
            user.latitude = latitude if latitude is not None else user.latitude
            user.longitude = longitude if longitude is not None else user.longitude

            db.session.add(user)
            db.session.commit()
            return 200, {'message': 'User updated successfully'}
        except Exception as e:
        # Rollback bei Fehlern
            db.session.rollback()
            return 500, {'message': 'Update failed', 'error': str(e)}

    @staticmethod
    def delete_user(id):
        try:
            user = User.query.get(id)
            if not user:
                return 404, {'message': 'User not found'}

            db.session.delete(user)
            db.session.commit()

            return 200, {'message': 'User deleted successfully'}

        except Exception as e:
            db.session.rollback()
            return 500, {'message': 'Delete failed', 'error': str(e)}

    

