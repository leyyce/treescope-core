from flask_restx.reqparse import RequestParser
from marshmallow import fields
from marshmallow.validate import Length

from app.auth.utils import RegisterSchema

pagination_parser = RequestParser()
pagination_parser.add_argument(
    "page", type=int, required=False, location='args', help="Page number"
)
pagination_parser.add_argument(
    "per_page", type=int, required=False, location='args', help="Page size"
)

class UpdateSchema(RegisterSchema):
    password = fields.Str(required=False, validate=[Length(min=8, max=128)])