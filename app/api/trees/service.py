from app.models.tree import Tree
from app.api.measurements.service import MeasurementService
from app.extensions import db


class TreeService:

    @staticmethod
    def create_tree(data, user_id):
        
        tree_data = {
            "initial_creator_id": user_id,
            "tree_type_id": data.get("tree_type_id"),
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "health_status_id": data.get("health_status_id", 1),
        }

        new_tree = Tree(**tree_data)
        db.session.add(new_tree)
        db.session.commit()
        
        message, code, measurement = MeasurementService.create_measurement(data["measurement"], new_tree.id, user_id)
        if code != 201:
            return message, code
        message, code = MeasurementService.create_photo(data["files"], new_tree.id, user_id, measurement.id)
        if code != 201:
            return message, code
        return f"Tree created", 201

    @staticmethod
    def get_trees(user_id=None):

        query = Tree.query.options(db.joinedload(Tree.health_status))
        if user_id is not None:
            query = Tree.query.options(db.joinedload(Tree.health_status), db.joinedload(Tree.files)).filter(Tree.initial_creator_id == user_id)

        tree_pagination = query.paginate(error_out=False)
        resp = {
            'count': len(tree_pagination.items),
            'total': tree_pagination.total,
            'page': tree_pagination.page,
            'per_page': tree_pagination.per_page,
            'pages': tree_pagination.pages,
            'has_next': tree_pagination.has_next,
            'has_prev': tree_pagination.has_prev,
            'prev_num': tree_pagination.prev_num,
            'next_num': tree_pagination.next_num,
            'trees': tree_pagination.items,
        }
        return resp, 200
    
    @staticmethod
    def get_trees_wm(user_id):

        tree_pagination = Tree.query.options(db.joinedload(Tree.measurements),db.joinedload(Tree.health_status), db.joinedload(Tree.files)).filter(Tree.initial_creator_id == user_id).paginate(error_out=False)
        resp = {
            'count': len(tree_pagination.items),
            'total': tree_pagination.total,
            'page': tree_pagination.page,
            'per_page': tree_pagination.per_page,
            'pages': tree_pagination.pages,
            'has_next': tree_pagination.has_next,
            'has_prev': tree_pagination.has_prev,
            'prev_num': tree_pagination.prev_num,
            'next_num': tree_pagination.next_num,
            'tree_wm': tree_pagination.items,
        }
        return resp, 200

    @staticmethod
    def get_tree_by_id(tree_id):
        tree = Tree.query.options(db.joinedload(Tree.measurements), db.joinedload(Tree.health_status), db.joinedload(Tree.files)).filter_by(id=tree_id).first()
        if not tree:
            return 'Tree not found', 404
        return tree, 200

    @staticmethod
    def update_tree(tree_data, tree_id):

        tree, code = TreeService.get_tree_by_id(tree_id)
        if code == 404 or tree_id != tree.id:
            return f"Tree with ID {tree_id} does not exist", 404
        
        ## Optional values
        tree.tree_type = tree_data.get('tree_type', tree.tree_type)
        tree.health_status_id = tree_data.get('health_status_id')
        tree.latitude = tree_data.get('latitude', tree.latitude)
        tree.longitude = tree_data.get('longitude', tree.latitude)
        db.session.commit()

        return tree, 200
