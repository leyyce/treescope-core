from app.models.user import User

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
