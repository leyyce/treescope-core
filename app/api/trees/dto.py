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

    tree_photo = ns.model('tree_photo', {
        'id': fields.Integer(readonly=True, description='Photo unique identifier'),
        'treeid': fields.Integer(required=True, description='Related tree ID'),
        'measurementid': fields.Integer(required=True, description='Related measurement ID'),
        'userid': fields.Integer(required=False, description='Related user ID'),
        'photopath': fields.String(required=True, description='Path to the photo'),
        'description': fields.String(required=False, description='Photo description'),
        'uploadedat': fields.DateTime(readonly=True, description='Photo upload date'),
    })

    tree_photo_create = ns.model('tree_photo', {
        'filename': fields.String(required=False, description='filename'),
        'photodata': fields.String(required=False, description='uploadedphoto'),
        'description': fields.String(required=False, description='Photo description'),
    })

    tree = ns.model('tree', {
        'id': fields.Integer(readonly=True, description='Tree unique identifier', attribute='id'),
        'initialcreatorid': fields.Integer(required=True, description='Initial creator ID'),
        'treetype': fields.String(required=False, desScription='Type of tree'),
        'latitude': fields.Float(required=True, description='Tree latitude'),
        'longitude': fields.Float(required=True, description='Tree longitude'),
        'co2stored': fields.Float(default=0.00, description='CO2 stored by the tree in kg'),
        'healthstatus': fields.Integer(description='Tree health status'),
        'environmentalimpact': fields.Float(default=0.00, description='Environmental impact score'),
        'createdat': fields.DateTime(readonly=True, description='Tree creation date'),
        
        'healthstatusinfo': fields.Nested(health_status, description='Tree health statusinfo'),
        'files': fields.List(fields.Nested(tree_photo), required=False),

    })

    tree_create = ns.model('tree', {
        'treetype': fields.String(required=False, desScription='Type of tree'),
        'latitude': fields.Float(required=False, description='Tree latitude'),
        'longitude': fields.Float(required=False, description='Tree longitude'),
        'healthstatus': fields.Integer(required=False, description='Tree health status'),
        'measurements': fields.List(fields.Nested(MeasurementDto.create_measurement), required=False),
        'files': fields.List(fields.Nested(tree_photo_create), required=False),

    })

    tree_wm = ns.model('tree_wm', {
        'id': fields.Integer(readonly=True, description='Tree unique identifier'),
        'initialcreatorid': fields.Integer(required=True, description='Initial creator ID'),
        'treetype': fields.String(required=False, description='Type of tree'),
        'latitude': fields.Float(required=True, description='Tree latitude'),
        'longitude': fields.Float(required=True, description='Tree longitude'),
        'co2stored': fields.Float(default=0.00, description='CO2 stored by the tree in kg'),
        'healthstatus': fields.Integer(description='Tree health status'),
        'environmentalimpact': fields.Float(default=0.00, description='Environmental impact score'),
        'createdat': fields.DateTime(readonly=True, description='Tree creation date'),
        'measurements': fields.List(fields.Nested(MeasurementDto.measurement)),
        'healthstatusinfo': fields.Nested(health_status, description='Tree health statusinfo'),
        'files': fields.List(fields.Nested(tree_photo), required=False),
    })

    tree_update = ns.model('tree_update', {
        'id': fields.Integer(readonly=True, required=True, description='Tree unique identifier'),
        'treetype': fields.String(required=False, description='Type of tree'),
        'latitude': fields.Float(required=False, description='Tree latitude'),
        'longitude': fields.Float(required=False, description='Tree longitude'),
        'healthstatus': fields.String(required=False, description='Tree health status'),
    })

    tree_page = ns.clone('tree_page', pagination_base, {
        'trees': fields.List(fields.Nested(tree, many=True, skip_none=True))
    })

    tree_page_wm = ns.clone('tree_page_wm', pagination_base, {
        'tree_wm': fields.List(fields.Nested(tree_wm, many=True, skip_none=True))
    })

   