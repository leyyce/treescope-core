from flask import request
from flask_praetorian.exceptions import PraetorianError
from flask_restx import Resource
from .dto import AuthDto
from .utils import LoginSchema, RegisterSchema
from .service import AuthService
from ..api.users.dto import UserDto

login_schema = LoginSchema()
register_schema = RegisterSchema()

ns = AuthDto.ns
user_ns = UserDto.ns
auth_success = AuthDto.auth_success


@ns.route('/login')
class AuthLogin(Resource):
    """ User login endpoint
    User registers then receives the user's information and access_token
    """

    auth_login = AuthDto.auth_login

    @ns.doc(
        'Auth login',
        responses={
            200: ('Logged in', auth_success),
            400: 'Validations failed.',
            403: 'Incorrect password or wrong username.',
            404: 'Email does not match any account.',
        },
    )
    @ns.expect(auth_login, validate=True)
    @ns.marshal_with(auth_success)
    def post(self):
        """ Login using email and password """
        # Grab the json data
        login_data = request.get_json()

        # Validate data
        if errors := login_schema.validate(login_data):
            ns.abort(400, errors)
        response, code = AuthService.login(login_data)
        if code != 200:
            ns.abort(code, response)
        return response, code


@ns.route('/register')
class AuthRegister(Resource):
    """ User register endpoint
    User registers then receives the user's information and access_token
    """

    auth_register = AuthDto.auth_register

    @ns.doc(
        'Auth registration',
        responses={
            201: ('Successfully registered user.', auth_success),
            400: 'Malformed data or validations failed.',
            401: 'Email or username already exists.'
        },
    )
    @ns.expect(auth_register, validate=True)
    @ns.marshal_with(auth_success, code=201)
    def post(self):
        """ User registration """
        # Grab the json data
        register_data = request.get_json()

        # Validate data
        if errors := register_schema.validate(register_data):
            ns.abort(400, errors)
        response, code = AuthService.register(register_data)
        if code != 201:
            ns.abort(code, response)
        return response, code


@user_ns.errorhandler(PraetorianError)
def handle_praetorian_error(error):
    """Return a custom message and status code when the user did not provide a JWT"""
    return PraetorianError.build_error_handler_for_flask_restx()(error)
