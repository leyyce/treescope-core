from flask_restx.reqparse import RequestParser
from flask_wtf import FlaskForm
from marshmallow import Schema, fields, ValidationError, validates_schema
from marshmallow.validate import Regexp, Length, Range
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Regexp as RegexpWTForms, Length as LengthWTForms

finalization_parser = RequestParser()
finalization_parser.add_argument(
    "token", type=str, required=True, location='args', help="Registration token"
)

mail_change_parser = RequestParser()
mail_change_parser.add_argument(
    "token", type=str, required=True, location='args', help="Mail change token"
)

password_reset_parser = RequestParser()
password_reset_parser.add_argument(
    "token", type=str, required=True, location='args', help="Password reset token"
)

def validate_decimal_precision(value, max_digits, decimal_places):
    value_str = format(value, 'f')  # Convert Decimal to string without scientific notation
    integer_part, _, fractional_part = value_str.partition('.')

    if len(integer_part.lstrip('-')) > (max_digits - decimal_places):
        raise ValidationError(f"Value {value} exceeds max digits ({max_digits - decimal_places} before decimal).")
    if len(fractional_part) > decimal_places:
        raise ValidationError(f"Value {value} exceeds max decimal places ({decimal_places}).")

password_field = fields.Str(required=True, validate=[Length(min=8, max=128)])

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

    step_length = fields.Integer(required=True, validate=[Range(min=60, max=90)])

    password = password_field

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

class MailSchema(RegisterSchema):
    """ /auth/request-validation [POST]

    Parameters:
    - Email
    """
    class Meta:
        exclude = ('username', 'password', 'first_name', 'last_name', 'step_length', 'latitude', 'longitude')

class MailChangeSchema(RegisterSchema):
    """ /auth/change-mail [PATCH]

        Parameters:
        - Email
        - Password (Str)
    """

    class Meta:
        exclude = ('username', 'first_name', 'last_name', 'step_length', 'latitude', 'longitude')

class PasswordChangeSchema(Schema):
    """ /auth/change-password [PATCH]

    Parameters:
    - Old Password (Str)
    - New Password (Str)
    """

    old_password = password_field
    new_password = password_field

class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired(), LengthWTForms(min=8, max=128)])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Confirm Password Reset")
