from flask_praetorian import auth_required, current_user
from flask_restx import Resource
from flask import request

from .service import UserService
from .dto import UserDto
from .utils import pagination_parser, UpdateSchema

update_schema = UpdateSchema()

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
    @auth_required
    def get(self):
        """get a paginated list of all registered users"""
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
        """get a user given its ID"""
        # guard.get_user_from_registration_token()
        user = UserService.get_user(id)
        if not user:
            ns.abort(404, f"User with id '{id}' not found")
        return user
    
    @ns.doc(
        'Update a specific user',
        responses={
            200: 'User updated successfully',
            400: 'Validations failed.',
            401: 'Unauthorized',
            403: 'Email or username already exists.',
            404: 'User not found!',
        },
        security='jwt_header',
    )
    @ns.expect(UserDto.user_update, validate=True)
    @ns.marshal_with(UserDto.user)
    @auth_required
    def patch(self, id):
        """update user data"""
        user_data = request.get_json()
        if errors := update_schema.validate(user_data):
            ns.abort(400, errors)

        user = current_user()

        if not user:
            ns.abort(401, "User not logged in or user that is logged in doesn't exist anymore.")

        if 'Admin' in user.rolenames or user.id == id:
            response, code = UserService.update_user(id, user_data)
            if code != 200:
                ns.abort(code, response)
            return response, code
        ns.abort(401, 'Access denied, unauthorized user')
    
    @ns.doc(
        'Delete a specific user',
        responses={
            200: 'User deleted successfully',
            401: 'Unauthorized',
            404: 'User not found!',
        },
        security='jwt_header',
    )
    @auth_required
    def delete(self, id):
        """delete user data"""

        user = current_user()

        if not user:
            ns.abort(401, "User not logged in or user that is logged in doesn't exist anymore.")

        if 'Admin' in user.rolenames or user.id == id:
            response, code = UserService.delete_user(id)
            return response, code
        ns.abort(401, 'Access denied, unauthorized user')
