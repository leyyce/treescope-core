from flask import Blueprint
from flask_restx import Api

from .users.controller import ns as user_ns

api_v1_pb = Blueprint('api_v1', __name__)

api = Api(
    api_v1_pb,
    title='treescope',
    version='1.0',
    description='Treescope API - Version 1.0 provides endpoints for user operations and more.',
)

api.add_namespace(user_ns)