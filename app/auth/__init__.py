from flask import Blueprint
from flask_restx import Api

from .controller import ns as auth_ns

auth_pb = Blueprint('auth', __name__)

api = Api(
    auth_pb,
    title='treescope auth service',
    version='1.0',
    description='Authenticate and receive tokens.',
)

api.add_namespace(auth_ns)
