from flask_restx import Namespace, fields
from app.api.dto import pagination_base


class UserDto:
    ns = Namespace('users', description='User related operations')

    role = ns.model('role', {
        'id': fields.Integer(readonly=True, description='role unique identifier', attribute='role_id'),
        'name': fields.String(required=True, description='role name'),
        'description': fields.String(required=True, description='role description'),
    })

    user = ns.model('user', {
        'id': fields.Integer(readonly=True, description='user unique identifier'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='username'),
        'first_name': fields.String(required=False, description='first name'),
        'last_name': fields.String(required=False, description='last name'),
        'step_length': fields.Integer(required=True, description='step length'),
        'verified': fields.Boolean(readonly=True, required=False, description='user email verified'),
        'trust_level': fields.Integer(readonly=True, required=False, description='user trust level'),
        'roles': fields.List(fields.Nested(role, many=True, skip_none=True), readonly=True, required=False, description='user roles'),
        'latitude': fields.Float(required=False, description='user latitude'),
        'longitude': fields.Float(required=False, description='user longitude'),
        'created_at': fields.DateTime(readOnly=True, description='user creation date'),
        'updated_at': fields.DateTime(readOnly=True, description='user last update date'),
    })

    user_update = ns.model('user_update', {
        'username': fields.String(required=True, description='username'),
        'first_name': fields.String(required=False, description='first name'),
        'last_name': fields.String(required=False, description='last name'),
        'step_length': fields.Integer(required=True, description='step length'),
        'latitude': fields.String(required=False, description='user latitude'),
        'longitude': fields.String(required=False, description='user longitude'),
    })

    user_page = ns.clone('user_page', pagination_base, {
        'users': fields.List(fields.Nested(user, many=True, skip_none=True)),
    })
