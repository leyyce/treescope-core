from flask import Blueprint
from flask_restx import Api

from ..dto import pagination_base
from .controller import ns as tree_ns
from ...utils import jwt_authorizations_doc
from app.api.measurements.dto import MeasurementDto

api_tree = Blueprint('tree', __name__)

api = Api(
    api_tree,
    title='treescope',
    version='1.0',
    description='Tree operations and more.',
    authorizations=jwt_authorizations_doc
)

api.add_model('pagination_base', pagination_base)

api.add_namespace(tree_ns)
api.add_namespace(MeasurementDto.ns)
