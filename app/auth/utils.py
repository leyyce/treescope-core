from marshmallow import Schema, fields, ValidationError, validates_schema
from marshmallow.validate import Regexp, Length

from ..extensions import guard
from ..models.user import User


def validate_decimal_precision(value, max_digits, decimal_places):
    value_str = format(value, 'f')  # Convert Decimal to string without scientific notation
    integer_part, _, fractional_part = value_str.partition('.')

    if len(integer_part.lstrip('-')) > (max_digits - decimal_places):
        raise ValidationError(f"Value {value} exceeds max digits ({max_digits - decimal_places} before decimal).")
    if len(fractional_part) > decimal_places:
        raise ValidationError(f"Value {value} exceeds max decimal places ({decimal_places}).")


def get_user_from_token(token):
    """
    Gets a user based on the registration token that is supplied. Verifies
    that the token is a regisration token and that the user can be properly
    retrieved
    """
    data = guard.extract_jwt_token(token)
    user_id = data.get("id")
    if user_id is None:
        return None
    user = User.query.get(user_id)
    return user

class LoginSchema(Schema):
    """ /auth/login [POST]

    Parameters:
    - Username (Str)
    - Password (Str)
    """

    username = fields.Str(required=True, validate=[Length(min=4, max=15)])
    password = fields.Str(required=True, validate=[Length(min=8, max=128)])

# Validations with Marshmallow

class RegisterSchema(Schema):
    """ /auth/register [POST]

    Parameters:
    - Email
    - Username (Str)
    - First Name (Str)
    - Last Name (Str)
    - Password (Str)
    - Latitude (Float)
    - Longitude (Float)
    """

    email = fields.Email(required=True, validate=[Length(max=64)])
    username = fields.Str(
        required=True,
        validate=[
            Length(min=4, max=15),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid username!",
            ),
        ],
    )

    first_name = fields.Str(
        validate=[
            Regexp(
                r"^[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*$", error="Invalid name!",
            )
        ]
    )

    last_name = fields.Str(
        validate=[
            Regexp(
                r"^[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*$", error="Invalid name!",
            )
        ]
    )
    password = fields.Str(required=True, validate=[Length(min=8, max=128)])

    latitude = fields.Decimal(
        as_string=True,
        required=False,
        validate=[
            lambda value: Regexp(
                r"^[\+-]?(([1-8]?[0-9])(\.\d{1,6})?|90)\D*[NSns]?$", error="Invalid latitude!",
            )(str(value)),
            lambda value: validate_decimal_precision(value, 8, 6),
        ],
    )
    longitude = fields.Decimal(
        as_string=True,
        required=False,
        validate=[
            lambda value: Regexp(
                r"^[\+-]?((1[0-7][0-9]|[1-9]?[0-9])(\.\d{1,6})?|180)\D*[EWew]?$",
                error="Invalid longitude!",
            )(str(value)),
            lambda value: validate_decimal_precision(value, 9, 6),
        ],
    )

    @validates_schema
    def validate_required_fields(self, data, **kwargs):
        if 'latitude' in data and 'longitude' not in data:
            raise ValidationError('Provided latitude without longitude.')
        if 'longitude' in data and 'latitude' not in data:
            raise ValidationError('Provided longitude without latitude.')
