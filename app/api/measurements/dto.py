from flask_restx import Namespace, fields
from app.api.dto import pagination_base

class MeasurementDto:
    ns = Namespace('measurements', description='Measurement related operations')

    tree_photo = ns.model('tree_photo', {
        'id': fields.Integer(readonly=True, description='Photo unique identifier'),
        'tree_id': fields.Integer(required=True, description='Related tree ID'),
        'measurement_id': fields.Integer(required=True, description='Related measurement ID'),
        'user_id': fields.Integer(required=False, description='Related user ID'),
        'photo_path': fields.String(required=True, description='Path to the photo'),
        'description': fields.String(required=False, description='Photo description'),
        'created_at': fields.DateTime(readonly=True, description='Photo upload date'),
    })

    tree_photo_create = ns.model('tree_photo_upload', {
        'filename': fields.String(required=True, description='filename'),
        'photo_data': fields.String(required=True, description='Base64 encoded photo data'),
        'description': fields.String(required=False, description='Photo description'),
    })

    measurement = ns.model('measurement', {
        'id': fields.Integer(readonly=True, description='Measurement unique identifier'),
        'tree_id': fields.Integer(required=True, description='Related tree ID'),
        'user_id': fields.Integer(required=False, description='Related user ID'),
        'height': fields.Float(required=True, description='Height of the tree in meters'),
        'inclination': fields.Integer(required=True, description='Inclination angle in degrees'),
        'trunk_diameter': fields.Float(required=True, description='Trunk diameter in meters'),
        'notes': fields.String(required=False, description='Additional notes'),
        'created_at': fields.DateTime(readonly=True, description='Measurement collection date'),
    })

    measurement_with_files = ns.model('measurement_with_files', {
        'id': fields.Integer(readonly=True, description='Measurement unique identifier'),
        'tree_id': fields.Integer(required=True, description='Related tree ID'),
        'user_id': fields.Integer(required=False, description='Related user ID'),
        'height': fields.Float(required=True, description='Height of the tree in meters'),
        'inclination': fields.Integer(required=True, description='Inclination angle in degrees'),
        'trunk_diameter': fields.Float(required=True, description='Trunk diameter in meters'),
        'notes': fields.String(required=False, description='Additional notes'),
        'created_at': fields.DateTime(readonly=True, description='Measurement collection date'),
        'files': fields.List(fields.Nested(tree_photo), required=False),
    })

    create_measurement = ns.model('create_measurement', {
        'height': fields.Float(required=True, description='Height of the tree in meters'),
        'inclination': fields.Integer(required=True, description='Inclination angle in degrees'),
        'trunk_diameter': fields.Float(required=True, description='Trunk diameter in meters'),
        'notes': fields.String(required=False, description='Additional notes'),
    })

    create_measurement_with_files = ns.model('create_measurement_with_files', {
        'height': fields.Float(required=True, description='Height of the tree in meters'),
        'inclination': fields.Integer(required=True, description='Inclination angle in degrees'),
        'trunk_diameter': fields.Float(required=True, description='Trunk diameter in meters'),
        'notes': fields.String(required=False, description='Additional notes'),
        'files': fields.List(fields.Nested(tree_photo_create), required=False),
    })
