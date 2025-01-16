from flask_praetorian import auth_required
from flask_restx import Resource
from flask import request

from app.extensions import guard
from .service import UserService
from .dto import UserDto
from .utils import UserSchema, UserUpdSchema

user_schema_upd = UserUpdSchema()
ns = UserDto.ns


@ns.route('/<int:id>')
@ns.param('id', 'The user identifier')
class User(Resource):

    user_ = UserDto.user_update

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
    
    @ns.doc(
        'Update a specific user',
        responses={
            200: 'User updated successfully',
            403: 'Unauthorized',
            404: 'User not found!',
            500: 'Update failed'
        },
        security='jwt_header',
    )
    @ns.expect(user_, validate=True)
    @auth_required
    def put(self, id):
        """update user data"""
        data_ = request.get_json()
        if errors := user_schema_upd.validate(data_):
            ns.abort(400, errors)
        
        # Token aus dem Authorization-Header extrahieren
        token = guard.read_token_from_header()
        # Token-Daten dekodieren
        token_data = guard.extract_jwt_token(token)
        # Benutzer-ID aus dem Payload abrufen
        user_id = token_data.get('id')
        roles = token_data.get('rls', [])

        if 'Admin' in roles:
            response, code = UserService.update_user(data_, id)
            return code, response
        elif(user_id == id):
            response, code = UserService.update_user(data_, id)
            return code, response
        else:
            ns.abort(403, f"Access Denied, Unauthorized User")
    
    @ns.doc(
        'Delete a specific user',
        responses={
            200: 'User deleted successfully',
            403: 'Unauthorized',
            404: 'User not found!',
            500: 'Delete failed' 
        },
        security='jwt_header',
    )
    @auth_required
    def delete(self, id):
        """delete user data"""

        # Token aus dem Authorization-Header extrahieren
        token = guard.read_token_from_header()
        # Token-Daten dekodieren
        token_data = guard.extract_jwt_token(token)
        # Benutzer-ID aus dem Payload abrufen
        user_id = token_data.get('id')
        roles = token_data.get('rls', [])

        if 'Admin' in roles:
            response, code = UserService.delete_user(id)
            return code, response
        elif(user_id == id):
            response, code = UserService.delete_user(id)
            return code, response
        else:
            ns.abort(403, f"Access Denied, Unauthorized User")



