from marshmallow.validate import Regexp
from marshmallow import Schema, fields, validate
from marshmallow.fields import Nested

from app.auth.utils import validate_decimal_precision
from app.api.measurements.utils import TreePhotoSchema, MeasurementSchema

class TreeSchema(Schema):
    """  [POST]
     
    Parameters:
    - Latitude (Float)
    - Longitude (Float)
    - Health Status (String)
    """
    tree_type_id = fields.Integer(required=False, default=1)
    latitude = fields.Decimal(
        as_string=True,
        required=True,
        validate=[
            lambda value: Regexp(
                r"^[\+-]?(([1-8]?[0-9])(\.\d{1,6})?|90)\D*[NSns]?$", error="Invalid latitude!",
            )(str(value)),
            lambda value: validate_decimal_precision(value, 8, 6),
        ],
    )
    longitude = fields.Decimal(
        as_string=True,
        required=True,
        validate=[
            lambda value: Regexp(
                r"^[\+-]?((1[0-7][0-9]|[1-9]?[0-9])(\.\d{1,6})?|180)\D*[EWew]?$",
                error="Invalid longitude!",
            )(str(value)),
            lambda value: validate_decimal_precision(value, 9, 6),
        ],
    )
    health_status_id = fields.Integer(required=False, default=1)
    measurement = fields.Nested(MeasurementSchema, required=True)
    files = fields.List(Nested(TreePhotoSchema), required=True, validate=validate.Length(min=2))

class TreeUpdateSchema(Schema):
    """  [PATCH]
     
    Parameters:
    - Latitude (Float)
    - Longitude (Float)
    - Health Status (String)
    """

    id = fields.Integer(dump_only=True)
    tree_type_id = fields.Integer(required=False, default=1)
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
    health_status_id = fields.Integer(required=False, default=1)