from flask_restx import Namespace, fields
from app.api.dto import pagination_base

class MeasurementDto:
    ns = Namespace('measurements', description='Measurement related operations')

    measurement = ns.model('measurement', {
        'id': fields.Integer(readonly=True, description='Measurement unique identifier'),
        'treeid': fields.Integer(required=True, description='Related tree ID'),
        'userid': fields.Integer(required=False, description='Related user ID'),
        'suspectedtreetype': fields.String(required=False, description='Suspected tree type'),
        'height': fields.Float(required=True, description='Height of the tree in meters'),
        'inclination': fields.Integer(required=True, description='Inclination angle in degrees'),
        'trunkdiameter': fields.Float(required=True, description='Trunk diameter in meters'),
        'notes': fields.String(required=False, description='Additional notes'),
        'collectedat': fields.DateTime(readonly=True, description='Measurement collection date'),
    })

    create_measurement = ns.model('create_measurement', {
        'suspectedtreetype': fields.String(required=False, description='Suspected tree type'),
        'height': fields.Float(required=True, description='Height of the tree in meters'),
        'inclination': fields.Integer(required=True, description='Inclination angle in degrees'),
        'trunkdiameter': fields.Float(required=True, description='Trunk diameter in meters'),
        'notes': fields.String(required=False, description='Additional notes'),
    })

