from app.models.tree import Tree, HealthStatus, TreePhoto
from app.models.measurement import Measurement
from app.extensions import db, guard
from .utils import allowed_file, UPLOAD_FOLDER, generate_hashed_filename, save_base64_image



class TreeService:

    @staticmethod
    def create_tree(data, user_id):
        
        tree_data = {
            "initialcreatorid": user_id,
            "treetype": data.get("treetype"),
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "healthstatus": data.get("healthstatus", 1),
            "co2stored": data.get("co2stored", 0.00),
            "environmentalimpact": data.get("environmentalimpact", 0.00)
        }

        new_tree = Tree(**tree_data)
        db.session.add(new_tree)
        db.session.commit()
        message = "Added : Tree Data successfully,"


        measurements_data = data.get("measurements", [])  # Liste von Messungen
        if measurements_data == []:
            message = message + "measurements failed,"
        new_measurements = []

        for measurement_data in measurements_data:

            measurement_data["treeid"] = new_tree.id  
            measurement_data["userid"] = user_id
            
            # Erstelle eine neue Measurement-Instanz
            new_measurement = Measurement(**measurement_data)
            new_measurements.append(new_measurement)
            db.session.add(new_measurement)
            db.session.commit()
            message = message + "measurement successfully,"
        
        files = data.get("files")
        if files != None:
            for file_data in files:

                if file_data.get("photodata") == '':
                    message = message + "photodata failed,"
                    continue

                if allowed_file(file_data.get("filename")):
                    filename = generate_hashed_filename(file_data.get("filename"), user_id, new_tree.id)
                    file_path = save_base64_image(file_data.get("photodata"), filename)
                    if(file_path == None):
                        message = message + f'photodata {file_data.get("filename")} failed,'
                        continue

                    new_photo = TreePhoto(
                    treeid=new_tree.id,
                    measurementid=new_measurement.id,
                    userid=user_id,
                    photopath=file_path,
                    description=file_data.get('description'))

                    db.session.add(new_photo)
                    db.session.commit()
                    message = message + "photodata successfully."

        return message, 201

    @staticmethod
    def get_trees(user_id=None):

        query = Tree.query.options(db.joinedload(Tree.healthstatusinfo))
        if user_id is not None:
            query = Tree.query.options(db.joinedload(Tree.healthstatusinfo), db.joinedload(Tree.files)).filter(Tree.initialcreatorid == user_id)

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

        tree_pagination = Tree.query.options(db.joinedload(Tree.measurements),db.joinedload(Tree.healthstatusinfo), db.joinedload(Tree.files)).filter(Tree.initialcreatorid == user_id).paginate(error_out=False)
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
        tree = Tree.query.options(db.joinedload(Tree.measurements), db.joinedload(Tree.healthstatusinfo), db.joinedload(Tree.files)).filter_by(id=tree_id).first()
        if not tree:
            return 'Tree not found', 404
        return tree, 200

    @staticmethod
    def update_tree(tree_data, tree_id):

        tree, code = TreeService.get_tree_by_id(tree_id)
        if code == 404 or tree_id != tree.id:
            return f"Tree with ID {tree_id} does not exist", 404
        
        ## Optional values
        tree.treetype = tree_data.get('treetype', tree.latitude)
        healthstatus = tree_data.get('healthstatus')
        if(healthstatus):
            healthstatus = HealthStatus.query.filter_by(status=healthstatus).first()
            tree.healthstatus = healthstatus.id
        tree.latitude = tree_data.get('latitude', tree.latitude)
        tree.longitude = tree_data.get('longitude', tree.latitude)
        db.session.commit()

        return tree, 200
