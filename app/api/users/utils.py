from flask_restx.reqparse import RequestParser

from app.auth.utils import RegisterSchema

pagination_parser = RequestParser()
pagination_parser.add_argument(
    "page", type=int, required=False, location='args', help="Page number"
)
pagination_parser.add_argument(
    "per_page", type=int, required=False, location='args', help="Page size"
)

class UpdateSchema(RegisterSchema):
    class Meta:
        exclude = ('email', 'password')
