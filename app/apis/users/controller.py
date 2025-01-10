from flask_restx import Resource

from .service import UserService
from .dto import UserDto

ns = UserDto.ns

@ns.route('/<string:username>')
@ns.param('username', 'The username')
class User(Resource):
    @ns.doc(
        "Get a specific user",
        responses={
            200: ("User data successfully sent", UserDto.user),
            404: "User not found!",
        },
    )
    @ns.marshal_with(UserDto.user)
    def get(self, username):
        """get a user given its username"""
        user = UserService.get_user(username)
        if not user:
            ns.abort(404)
        return user