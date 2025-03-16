from flask import request
from flask_restx import Resource
from flask_praetorian import auth_required, current_user, auth_accepted, roles_required, PraetorianError

from .utils import TreeUpdateSchema, TreeSchema

from .service import TreeService
from .dto import TreeDto
from app.api.users.utils import pagination_parser

ns = TreeDto.ns

tree_update_schema = TreeUpdateSchema()
tree_schema = TreeSchema()

@ns.route('/create-tree')
class CreateTree(Resource):
    @ns.doc(
        'Tree and measurement creation',
        responses={
            201: 'Tree created',
            400: 'Malformed data or validations failed.',
        },
        security='jwt_header',
    )
    @ns.expect(TreeDto.tree_create)
    #@ns.expect(photo_upload_parser) funktioniert nicht
    @auth_accepted
    def post(self):
        """Create a Tree with measurements and photos"""
        data = request.get_json()
        try:
            user = current_user()
            user_id = user.id
        except PraetorianError as e:
            user_id = None
        if errors := tree_schema.validate(data):
            return errors, 400
        message, code = TreeService.create_tree(data, user_id)
        if code != 201:
            ns.abort(code, message)
        return message, code



@ns.route('/')
class TreeList(Resource):
    @ns.doc(
        'List of all registered trees from all users',
        responses={
            200: ('List of trees successfully sent', TreeDto.tree_page_wm)
        },
    )
    @ns.marshal_list_with(TreeDto.tree_page_wm)
    @ns.expect(pagination_parser)
    def get(self):
        """get a paginated list of all trees"""
        return TreeService.get_trees()

@ns.route('/user-tree')
class UserTreeList(Resource):
    @ns.doc(
        'List of all registered trees from one user w/o measurement',
        responses={
            200: ('List of trees successfully sent', TreeDto.tree_page),
            401: 'Unauthorized'
        },
        security='jwt_header',
    )
    @ns.marshal_list_with(TreeDto.tree_page)
    @ns.expect(pagination_parser)
    @auth_required
    def get(self):
        """Lists all trees with the user id."""
        user = current_user()
        if not user:
            return "User not logged in or user that is logged in doesn't exist anymore", 401 

        return TreeService.get_trees(user.id)


@ns.route('/user-tree-wm')
class UserTreeList(Resource):
    @ns.doc(
        'List of all registered trees from one user with measurements',
        responses={
            200: ('List of trees successfully sent', TreeDto.tree_page_wm),
            401: 'Unauthorized'
        },
        security='jwt_header',
    )
    @ns.marshal_list_with(TreeDto.tree_page_wm)
    @ns.expect(pagination_parser)
    @auth_required
    def get(self):
        """Lists all trees with the user id and the measurements."""
        user = current_user()
        if not user:
            return "User not logged in or user that is logged in doesn't exist anymore", 401 

        return TreeService.get_trees_wm(user.id)


@ns.route('/<int:id>')
@ns.param('id', 'The tree identifier')
class Tree(Resource):
    @ns.doc(
        'Get the data of a specific tree',
        responses={
            200: ('tree successfully send', TreeDto.tree_wm),
            404: 'Tree not found!',
        },
    )
    @ns.marshal_with(TreeDto.tree_wm)
    def get(self, id):
        """get the measurements for the tree id"""
        return TreeService.get_tree_by_id(id)

    @ns.doc(
        'Update a specific tree w/o measurement',
        responses={
            200: 'Tree updated successfully',
            400: 'Validations failed.',
            401: 'Unauthorized',
            404: 'Tree not found!',
        },
        security='jwt_header',
    )
    @ns.expect(TreeDto.tree_update)
    @ns.marshal_with(TreeDto.tree_wm)
    @roles_required('Admin')
    def patch(self, id):
        """update tree data"""
        tree_data = request.get_json()

        if errors := tree_update_schema.validate(tree_data):
            ns.abort(400, errors)

        message, code =  TreeService.update_tree(tree_data, id)
        if code != 200:
            ns.abort(code, message)
        return message, code

@ns.route('/types')
class TreeTypeList(Resource):
    @ns.doc(
        'List of all trees types',
        responses={
            200: ('List of tree types successfully sent', TreeDto.tree_type_page)
        },
    )
    @ns.marshal_list_with(TreeDto.tree_type_page)
    @ns.expect(pagination_parser)
    def get(self):
        """get a paginated list of all trees"""
        return TreeService.get_tree_types()