from flask import request, render_template, make_response
from flask_praetorian import auth_required
from flask_praetorian.constants import AccessType
from flask_praetorian.exceptions import PraetorianError, MissingClaimError
from flask_restx import Resource
from .dto import AuthDto
from .utils import LoginSchema, RegisterSchema, finalization_parser, MailSchema, MailChangeSchema, mail_change_parser
from .service import AuthService
from ..api.users.dto import UserDto
from app.extensions import db, guard

login_schema = LoginSchema()
register_schema = RegisterSchema()
mail_schema = MailSchema()
mail_change_schema = MailChangeSchema()

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
            401: 'Incorrect password or wrong username.',
            403: 'Email address not verified.',
        },
    )
    @ns.expect(auth_login, validate=True)
    @ns.marshal_with(auth_success)
    def post(self):
        """ Login using username and password """
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
    User registers then receives the user's information
    """

    auth_register = AuthDto.auth_register

    @ns.doc(
        'Auth registration',
        responses={
            201: ('Successfully registered user.', UserDto.user),
            400: 'Malformed data or validations failed.',
            403: 'Email or username already exists.'
        },
    )
    @ns.expect(auth_register, validate=True)
    @ns.marshal_with(UserDto.user, code=201)
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

@ns.route('/request-verification')
class RequestVerificationMail(Resource):
    """ Request verification mail endpoint
    User can request retransmission of verification mail
    """

    auth_mail = AuthDto.auth_mail

    @ns.doc(
        'Auth request verification mail',
        responses={
            200: 'Successfully send validation mail if user with mail address exists.',
            400: 'Malformed data or validations failed.',
            403: 'Mail already verified.'
        },
    )
    @ns.expect(auth_mail, validate=True)
    def post(self):
        """ Request verification mail """
        # Grab the json data
        request_verification_data = request.get_json()

        # Validate data
        if errors := mail_schema.validate(request_verification_data):
            ns.abort(400, errors)
        response, code = AuthService.send_validation_mail(request_verification_data)
        if code != 200:
            ns.abort(code, response)
        return response, code

@ns.route('/finalize', doc=False)
class AuthFinalize(Resource):
    @ns.expect(finalization_parser)
    def get(self):
        """ Finalize user """
        args = finalization_parser.parse_args()
        try:
            user = guard.get_user_from_registration_token(args['token'])
            user.verified = True
            db.session.commit()
            return make_response(render_template("auth/finalize_success.html",
                                                 name = user.first_name if user.first_name else user.username,
                                                 addr = user.email,
                                                 title="Verification success - TreeScope"
                                                 )
                                 )
        except PraetorianError as e:
            return make_response(render_template("auth/finalize_error.html",
                                                 error=e.message,
                                                 title="Verification failed - TreeScope"
                                                 )
                                 )
# TODO: Clean up and make settings available as env vars
@ns.route('/change-mail')
class AuthChangeMail(Resource):
    """ Change email address endpoint
    User can request to change the email address
    """
    auth_mail_change = AuthDto.auth_mail_change

    @ns.hide
    @ns.expect(mail_change_parser)
    def get(self):
        """ Finalize mail change """
        args = mail_change_parser.parse_args()
        token = args['token']
        try:
            user = guard.get_user_from_registration_token(token)
            data = guard.extract_jwt_token(token, access_type=AccessType.register)
            MissingClaimError.require_condition(
                "custom_claims" in data,
                "Token is missing custom_claims",
            )
            custom_claims = data['custom_claims']
            MissingClaimError.require_condition(
                "new_mail_address" in custom_claims,
                "Token is missing new_mail_address custom claim",
            )
            new_mail_address = custom_claims['new_mail_address']
            user.email = new_mail_address
            db.session.commit()
            return make_response(render_template("auth/mail_change_success.html",
                                                 name=user.first_name if user.first_name else user.username,
                                                 addr=user.email,
                                                 title="Mail change success - TreeScope"
                                                 )
                                 )
        except PraetorianError as e:
            return make_response(render_template("auth/mail_change_error.html",
                                                 error=e.message,
                                                 title="Mail change failed - TreeScope"
                                                 )
                                 )

    @ns.doc(
        'Auth request email change',
        responses={
            200: 'Successfully send mail change verification',
            400: 'Malformed data or validations failed.',
            403: 'Mail already in use.'
        },
        security='jwt_header',
    )
    @ns.expect(auth_mail_change)
    @auth_required
    def patch(self):
        """ Change user email address """
        mail_data = request.get_json()

        #Validate data
        if errors := mail_change_schema.validate(mail_data):
            ns.abort(400, errors)
        response, code = AuthService.request_mail_change(mail_data)
        if code != 200:
            ns.abort(code, response)
        return response, code


@ns.errorhandler(PraetorianError)
@user_ns.errorhandler(PraetorianError)
def handle_praetorian_error(error):
    """Return a custom message and status code when the user did not provide a JWT"""
    return PraetorianError.build_error_handler_for_flask_restx()(error)
