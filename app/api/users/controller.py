from flask_praetorian import auth_required, roles_required
from flask_restx import Resource

from .service import UserService
from .dto import UserDto
from .utils import pagination_parser

ns = UserDto.ns

@ns.route('/')
class UserList(Resource):
    @ns.doc(
        'List of all registered users',
        responses={
            200: ('List of users successfully sent', UserDto.user_page),
            401: 'Missing Authorization Header',
            403: 'Missing required roles',
        },
        security='jwt_header',
    )
    @ns.marshal_list_with(UserDto.user_page)
    @ns.expect(pagination_parser)
    @roles_required("Admin")
    def get(self):
        return UserService.get_users()

@ns.route('/<int:id>')
@ns.param('id', 'The user identifier')
class User(Resource):
    @ns.doc(
        'Get a specific user',
        responses={
            200: ('User data successfully sent', UserDto.user),
            404: 'User not found!',
        },
        security='jwt_header',
    )
    @ns.marshal_with(UserDto.user)
    @auth_required
    def get(self, id):
        """get a user given its username"""
        # guard.get_user_from_registration_token()
        user = UserService.get_user(id)
        if not user:
            ns.abort(404, f"User with id '{id}' not found")
        return user
