from flask_restx import Namespace, fields
from app.api.dto import pagination_base
from ..measurements.dto import MeasurementDto


class TreeDto:
    ns = Namespace('trees', description='Tree related operations')

    tree_type = ns.model('tree_type', {
        'id': fields.Integer(required=True, description='The tree type'),
        'name': fields.String(required=True, description='The tree name'),
        'scientific_name': fields.String(required=False, description='The tree scientific name'),
        'description': fields.String(required=False, description='The tree description'),
    })

    health_status = ns.model('health_status', {
        'id': fields.Integer(readonly=True, description='Health status unique identifier'),
        'name': fields.String(required=True, description='Health status name'),
        'description': fields.String(required=True, description='Health status description'),
    })

    tree = ns.model('tree', {
        'id': fields.Integer(readonly=True, description='Tree unique identifier', attribute='id'),
        'initial_creator_id': fields.Integer(required=True, description='Initial creator ID'),
        'tree_type_id': fields.Integer(required=False, desScription='Tree type ID'),
        'latitude': fields.String(required=True, description='Tree latitude'),
        'longitude': fields.String(required=True, description='Tree longitude'),
        'co2_stored': fields.Float(default=0.00, description='CO2 stored by the tree in kg'),
        'health_status_id': fields.Integer(description='Tree health status ID'),
        'created_at': fields.DateTime(readonly=True, description='Tree creation date'),
        'updated_at': fields.DateTime(readonly=True, description='Tree update date'),

        'tree_type': fields.Nested(tree_type, description='Tree type'),
        'health_status': fields.Nested(health_status, description='Tree health status'),
        'files': fields.List(fields.Nested(MeasurementDto.tree_photo), required=False),

    })

    tree_create = ns.model('tree', {
        'tree_type_id': fields.Integer(required=False, desScription='Tree type ID'),
        'latitude': fields.String(required=True, description='Tree latitude'),
        'longitude': fields.String(required=True, description='Tree longitude'),
        'health_status_id': fields.Integer(required=False, description='Tree health status ID'),
        'measurement': fields.Nested(MeasurementDto.create_measurement, required=True),
        'files': fields.List(fields.Nested(MeasurementDto.tree_photo_create), required=True),
    })

    tree_wm = ns.model('tree_wm', {
        'id': fields.Integer(readonly=True, description='Tree unique identifier'),
        'initial_creator_id': fields.Integer(required=True, description='Initial creator ID'),
        'tree_type_id': fields.Integer(required=False, description='Tree type ID'),
        'latitude': fields.String(required=True, description='Tree latitude'),
        'longitude': fields.String(required=True, description='Tree longitude'),
        'co2_stored': fields.Float(default=0.00, description='CO2 stored by the tree in kg'),
        'health_status_id': fields.Integer(description='Tree health status ID'),
        'created_at': fields.DateTime(readonly=True, description='Tree creation date'),
        'updated_at': fields.DateTime(readonly=True, description='Tree update date'),

        'tree_type': fields.Nested(tree_type, description='Tree type'),
        'measurements': fields.List(fields.Nested(MeasurementDto.measurement)),
        'health_status': fields.Nested(health_status, description='Tree health statusinfo'),
        'files': fields.List(fields.Nested(MeasurementDto.tree_photo), required=False),
    })

    tree_update = ns.model('tree_update', {
        'id': fields.Integer(readonly=True, required=True, description='Tree unique identifier'),
        'tree_type_id': fields.Integer(required=False, description='Type of tree'),
        'latitude': fields.String(required=False, description='Tree latitude'),
        'longitude': fields.String(required=False, description='Tree longitude'),
        'health_status_id': fields.Integer(required=False, description='Tree health status ID'),
    })

    tree_page = ns.clone('tree_page', pagination_base, {
        'trees': fields.List(fields.Nested(tree, many=True, skip_none=True))
    })

    tree_page_wm = ns.clone('tree_page_wm', pagination_base, {
        'tree_wm': fields.List(fields.Nested(tree_wm, many=True, skip_none=True))
    })

    tree_type_page = ns.clone('tree_type_page', pagination_base, {
        'tree_types': fields.List(fields.Nested(tree_type, many=True, skip_none=True))
    })

   