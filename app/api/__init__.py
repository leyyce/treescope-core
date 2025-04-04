from flask import Blueprint
from flask_restx import Api

from .dto import pagination_base
from .users.controller import ns as user_ns
from .trees.controller import ns as tree_ns
from .measurements.controller import ns as measurement_ns
from ..utils import jwt_authorizations_doc

api_v1_pb = Blueprint('api_v1', __name__)

api = Api(
    api_v1_pb,
    title='treescope',
    version='1.0',
    description='Treescope API - Version 1.0 provides endpoints for user operations and more.',
    authorizations=jwt_authorizations_doc
)

api.add_model('pagination_base', pagination_base)

api.add_namespace(user_ns)
api.add_namespace(tree_ns)
api.add_namespace(measurement_ns)
