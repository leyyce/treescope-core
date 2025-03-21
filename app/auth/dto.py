from flask_restx import Namespace, fields

from app.api.users.dto import UserDto


class AuthDto:
    ns = Namespace('auth', description='Authenticate and receive tokens.', path='/')
    ns.add_model('user', UserDto.user)
    ns.add_model('role', UserDto.role)

    auth_login = ns.model(
        'Login data',
        {
            'username': fields.String(requied=True),
            'password': fields.String(required=True),
        },
    )

    auth_register = ns.model(
        'Registration data',
        {
            'email': fields.String(required=True),
            'username': fields.String(required=True),
            'password': fields.String(required=True),
            'first_name': fields.String(required=False),
            'last_name': fields.String(required=False),
            'step_length': fields.Integer(required=True),
            'latitude': fields.String(required=False),
            'longitude': fields.String(required=False),
        },
    )

    auth_mail = ns.model(
        'Mail data',
        {
            'email': fields.String(required=True),
        }
    )

    auth_mail_change = ns.clone(
        "Mail change data",
        auth_mail,
        {
            'password': fields.String(required=True),
        }
    )

    auth_password_change = ns.model(
        'Password change data',
        {
            'old_password': fields.String(required=True),
            'new_password': fields.String(required=True),
        }
    )

    auth_success = ns.model(
        'Auth success response',
        {
            'access_token': fields.String,
            'user': fields.Nested(UserDto.user),
        },
    )
