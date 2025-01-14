from flask_praetorian import auth_required
from flask_restx import Resource

from .service import UserService
from .dto import UserDto

ns = UserDto.ns


@ns.route('/<int:id>')
@ns.param('id', 'The user identifier')
class User(Resource):
    @ns.doc(
        "Get a specific user",
        responses={
            200: ("User data successfully sent", UserDto.user),
            404: "User not found!",
        },
    )
    @ns.marshal_with(UserDto.user)
    @auth_required
    def get(self, id):
        """get a user given its username"""
        # guard.get_user_from_registration_token()
        user = UserService.get_user(id)
        if not user:
            ns.abort(404)
        else:
            return user
