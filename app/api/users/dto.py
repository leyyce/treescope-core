from flask_restx import Namespace, fields

from app.api.dto import pagination_base


class UserDto:
    ns = Namespace('users', description='User related operations')

    role = ns.model('role', {
        'id': fields.Integer(readOnly=True, description='role unique identifier', attribute='role_id'),
        'name': fields.String(required=True, description='role name'),
        'description': fields.String(required=True, description='role description'),
    })

    user = ns.model('user', {
        'id': fields.Integer(readOnly=True, description='user unique identifier'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='username'),
        'first_name': fields.String(required=False, description='first name'),
        'last_name': fields.String(required=False, description='last name'),
        'verified': fields.Boolean(required=False, description='user email verified'),
        'trust_level': fields.Integer(required=False, description='user trust level'),
        'roles': fields.List(fields.Nested(role, many=True, skip_none=True), description='user roles'),
        'latitude': fields.Float(required=False, description='user latitude'),
        'longitude': fields.Float(required=False, description='user longitude'),
        'created_at': fields.DateTime(readOnly=True, description='user creation date'),
        'updated_at': fields.DateTime(readOnly=True, description='user last update date'),
    })

    data_resp = ns.model(
        'User Data Response',
        {
            'status': fields.Boolean,
            'message': fields.String,
            'user': fields.Nested(user),
        })

    user_page = ns.inherit('user_page', pagination_base, {
        'users': fields.List(fields.Nested(user, many=True, skip_none=True)),
    })
