# Validations with Marshmallow
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Regexp, Length
from flask_restx.reqparse import RequestParser

pagination_parser = RequestParser()
pagination_parser.add_argument(
    "page", type=int, required=False, location='args', help="Page number"
)
pagination_parser.add_argument(
    "per_page", type=int, required=False, location='args', help="Page size"
)


class RoleSchema(Schema):
    """ 
    Parameters:
    - ID (Integer)
    - Name (Str)
    - Description (Str)
    """

    id = fields.Integer(readOnly=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)

class UserSchema(Schema):
    """
    Parameters:
    - ID (Integer)
    - Email (Str)
    - Username (Str)
    - First_Name (Str)
    - Last_Name (Str)
    - Verified (Boolean)
    - Trust_Level (Str)
    - Roles (List)
    - latitude (Float)
    - longitude (Float)
    - created_at (DateTime)
    - updated_at (DateTime)
    """
    id = fields.Integer(readOnly=True)
    email = fields.String(required=True)
    username = fields.String(required=True)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    verified = fields.Boolean(required=False)
    trust_level = fields.Integer(required=False)
    roles = fields.List(fields.Nested(RoleSchema, many=True, skip_none=True))
    latitude = fields.Float(required=False)
    longitude = fields.Float(required=False)
    created_at = fields.DateTime(readOnly=True)
    updated_at = fields.DateTime(readOnly=True)

class UserUpdSchema(Schema):
    """
    Parameters:
    - Email (Str)
    - Username (Str)
    - First_Name (Str)
    - Last_Name (Str)
    - latitude (Float)
    - longitude (Float)
    """
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    latitude = fields.Float(required=False)
    longitude = fields.Float(required=False)
   

class DataRespSchema(Schema):
    """
    Parameters:
    - Status (Boolean)
    - Message (Str)
    - User (UserSchema)
    """

    status = fields.Boolean
    message = fields.String
    user = fields.Nested(UserSchema)

