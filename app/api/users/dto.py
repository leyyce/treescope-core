from flask_restx import Namespace, fields


class UserDto:
    ns = Namespace('users', description='User related operations')

    role = ns.model('role', {
        id: fields.Integer(readOnly=True, description='role unique identifier', attribute='role_id'),
    })

    user = ns.model('user', {
        'id': fields.Integer(readOnly=True, description='user unique identifier'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='username'),
        'first_name': fields.String(required=False, description='first name'),
        'last_name': fields.String(required=False, description='last name'),
        'verified': fields.Boolean(required=False, description='user email verified'),
        'trust_level': fields.Integer(required=False, description='user trust level'),
        'latitude': fields.Float(required=False, description='user latitude'),
        'longitude': fields.Float(required=False, description='user longitude'),
        'created_at': fields.DateTime(readOnly=True, description='user creation date'),
        'updated_at': fields.DateTime(readOnly=True, description='user last update date'),
    })

    data_resp = ns.model(
        'User Data Response',
        {
            "status": fields.Boolean,
            "message": fields.String,
            "user": fields.Nested(user),
        })
