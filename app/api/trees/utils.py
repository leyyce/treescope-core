import os
import base64
import hashlib
from marshmallow.validate import Length, Regexp, OneOf
from marshmallow import Schema, fields, validate, validates_schema
from marshmallow.fields import Nested
from app.auth.utils import validate_decimal_precision
from decimal import Decimal
from werkzeug.utils import secure_filename
from flask_restx import reqparse
from werkzeug.datastructures import FileStorage


# Parser für Dateiupload
photo_upload_parser = reqparse.RequestParser()
photo_upload_parser.add_argument(
    'photo',
    type=FileStorage,
    location='files',
    required=True,
    help='Photo file to upload (PNG, JPG, JPEG)'
)
photo_upload_parser.add_argument(
    'description',
    type=str,
    required=False,
    help='Optional description for the photo'
)

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_hashed_filename(filedata, filename):
    # Sicheren Dateinamen generieren (entfernt Sonderzeichen und unsichere Zeichen)
    secure_name = secure_filename(filename)

    # Dateiendung extrahieren
    ext = os.path.splitext(secure_name)[1]

    # String erstellen, zum hashen
    hash_input = f"{filedata}{ext}"

    # Hash erzeugen (SHA-256)
    hash_object = hashlib.sha256(hash_input.encode())
    hashed_name = hash_object.hexdigest()
    
    # Hashed Name + Dateiendung zurückgeben
    return f"{hashed_name}{ext}"


def save_base64_image(base64_string, file_name):
    # Sicherstellen, dass der Zielordner existiert
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Pfad der Datei erstellen
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    try:
        # Entferne das Präfix 'data:image/<format>;base64,' (falls vorhanden)
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
        
        # Base64-String dekodieren
        image_data = base64.b64decode(base64_string)

        # Datei im Zielordner speichern
        with open(file_path, "wb") as file:
            file.write(image_data)

        return file_path  # Pfad der gespeicherten Datei zurückgeben
    except Exception as e:
        print(f"Fehler beim Speichern der Datei: {e}")
        return None


def encode_image_to_base64(file_path):
    
    try:
        # Bild im Binärmodus öffnen
        with open(file_path, "rb") as file:
            # Datei lesen und in Base64 enkodieren
            encoded_string = base64.b64encode(file.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"Fehler beim Enkodieren des Bildes: {e}")
        return None


class TreePhotoSchema(Schema):
    filename = fields.String(required=True)
    photo_data = fields.String(required=True)
    description = fields.String(required=False, validate=Length(max=256))
   
class MeasurementSchema(Schema):
    suspected_tree_type = fields.String(required=False, validate=validate.Length(max=128))
    height = fields.Decimal(
        required=True,
        validate=validate.Range(min=Decimal("0.01"))  # Höhe muss positiv sein
    )
    inclination = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=90)  # Neigung muss zwischen 0 und 90 liegen
    )
    trunk_diameter = fields.Decimal(
        required=True,
        validate=validate.Range(min=Decimal("0.01"))  # Durchmesser muss positiv sein
    )
    notes = fields.String(required=False, allow_none=True)


class TreeSchema(Schema):
    """  [POST]
     
    Parameters:
    - Latitude (Float)
    - Longitude (Float)
    - Health Status (String)
    """
    tree_type = fields.String(required=False, validate=validate.Length(max=128))
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
    health_status = fields.Integer(required=False, default=1)
    measurement = fields.Nested(MeasurementSchema, required=True)
    files = fields.List(Nested(TreePhotoSchema), required=True)

class TreeUpdateSchema(Schema):
    """  [PATCH]
     
    Parameters:
    - Latitude (Float)
    - Longitude (Float)
    - Health Status (String)
    """

    id = fields.Integer(dump_only=True)
    tree_type = fields.String(required=False, validate=validate.Length(max=128))
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
    health_status = fields.String(
        required=False,
        validate=OneOf(
            ["Unknown", "Unhealthy", "Healthy"],
            error="Invalid health status! Must be one of: 'Unknown', 'Unhealthy', 'Healthy'."
        ),
    )