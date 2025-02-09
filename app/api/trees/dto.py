from flask_restx import Namespace, fields
from app.api.dto import pagination_base
from ..measurements.dto import MeasurementDto


class TreeDto:
    ns = Namespace('trees', description='Tree related operations')

    health_status = ns.model('health_status', {
        'id': fields.Integer(readonly=True, description='Health status unique identifier'),
        'status': fields.String(required=True, description='Health status name'),
        'description': fields.String(required=True, description='Health status description'),
    })

    tree = ns.model('tree', {
        'id': fields.Integer(readonly=True, description='Tree unique identifier', attribute='id'),
        'initial_creator_id': fields.Integer(required=True, description='Initial creator ID'),
        'tree_type': fields.String(required=False, desScription='Type of tree'),
        'latitude': fields.String(required=True, description='Tree latitude'),
        'longitude': fields.String(required=True, description='Tree longitude'),
        'co2_stored': fields.Float(default=0.00, description='CO2 stored by the tree in kg'),
        'health_status': fields.Integer(description='Tree health status'),
        'environmental_impact': fields.Float(default=0.00, description='Environmental impact score'),
        'created_at': fields.DateTime(readonly=True, description='Tree creation date'),
        'updated_at': fields.DateTime(readonly=True, description='Tree update date'),

        
        'health_status_info': fields.Nested(health_status, description='Tree health statusinfo'),
        'files': fields.List(fields.Nested(MeasurementDto.tree_photo), required=False),

    })

    tree_create = ns.model('tree', {
        'tree_type': fields.String(required=False, desScription='Type of tree'),
        'latitude': fields.String(required=True, description='Tree latitude'),
        'longitude': fields.String(required=True, description='Tree longitude'),
        'health_status': fields.Integer(required=False, description='Tree health status'),
        'measurement': fields.Nested(MeasurementDto.create_measurement, required=True),
        'files': fields.List(fields.Nested(MeasurementDto.tree_photo_create), required=True),
    })

    tree_wm = ns.model('tree_wm', {
        'id': fields.Integer(readonly=True, description='Tree unique identifier'),
        'initial_creator_id': fields.Integer(required=True, description='Initial creator ID'),
        'tree_type': fields.String(required=False, description='Type of tree'),
        'latitude': fields.String(required=True, description='Tree latitude'),
        'longitude': fields.String(required=True, description='Tree longitude'),
        'co2_stored': fields.Float(default=0.00, description='CO2 stored by the tree in kg'),
        'health_status': fields.Integer(description='Tree health status'),
        'environmental_impact': fields.Float(default=0.00, description='Environmental impact score'),
        'created_at': fields.DateTime(readonly=True, description='Tree creation date'),
        'updated_at': fields.DateTime(readonly=True, description='Tree update date'),
        'measurements': fields.List(fields.Nested(MeasurementDto.measurement)),
        'health_status_info': fields.Nested(health_status, description='Tree health statusinfo'),
        'files': fields.List(fields.Nested(MeasurementDto.tree_photo), required=False),
    })

    tree_update = ns.model('tree_update', {
        'id': fields.Integer(readonly=True, required=True, description='Tree unique identifier'),
        'tree_type': fields.String(required=False, description='Type of tree'),
        'latitude': fields.String(required=False, description='Tree latitude'),
        'longitude': fields.String(required=False, description='Tree longitude'),
        'health_status': fields.String(required=False, description='Tree health status'),
    })

    tree_page = ns.clone('tree_page', pagination_base, {
        'trees': fields.List(fields.Nested(tree, many=True, skip_none=True))
    })

    tree_page_wm = ns.clone('tree_page_wm', pagination_base, {
        'tree_wm': fields.List(fields.Nested(tree_wm, many=True, skip_none=True))
    })

   