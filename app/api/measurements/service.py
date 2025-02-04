import os
from app.models.measurement import Measurement,TreePhoto
from app.extensions import db, guard
from app.api.measurements.utils import allowed_file, UPLOAD_FOLDER, generate_hashed_filename, save_base64_image

class MeasurementService:
    @staticmethod
    def create_measurement(data, tree_id, user_id):
        
        measurement_data = data
        measurement_data["tree_id"] = tree_id
        measurement_data["user_id"] = user_id
            
        new_measurement = Measurement(**measurement_data)
        db.session.add(new_measurement)
        db.session.commit()

        return f"Added Measurement successful", 201, new_measurement
    
    @staticmethod
    def create_photo(data, tree_id, user_id, measurement_id):
        files = data
        if files is not None:
            for file_data in files:
                photo_data = file_data.get("photo_data")
                original_filename = file_data.get("filename")
                if photo_data == '':
                    return f"no photo_data found", 400

                if allowed_file(original_filename):
                    filename = generate_hashed_filename(photo_data, original_filename)
                    file_path = save_base64_image(photo_data, filename)
                    if file_path is None:
                        return f'photodata {file_data.get("filename")} failed', 400

                    new_photo = TreePhoto(
                    tree_id=tree_id,
                    measurement_id=measurement_id,
                    user_id=user_id,
                    photo_path=filename,
                    description=file_data.get('description'))

                    db.session.add(new_photo)
                    db.session.commit()

            return f"Created Photo", 201
        return f"Something went wrong", 400

    @staticmethod   
    def get_measurements_from_tree(id):
        return Measurement.query.options(db.joinedload(Measurement.files)).filter_by(tree_id=id).order_by(Measurement.created_at.desc()).all()
        

    @staticmethod
    def delete_measurement(id):
        measurement = Measurement.query.get(id)
        if not measurement:
            return f"Measurement not found", 404
        db.session.delete(measurement)
        db.session.commit()
        return f"Measurement deleted", 200
    
    @staticmethod
    def delete_photos(measurement_id):
        photos = TreePhoto.query.filter(TreePhoto.measurement_id == measurement_id).all()

        # Überprüfe jedes Foto, ob es noch in anderen Messungen vorkommt
        for photo in photos:
            other_references = TreePhoto.query.filter(TreePhoto.photo_path == photo.photo_path).count()

            # Falls es keine weiteren Referenzen gibt, lösche die Datei
            if other_references == 1:
                try:
                    photo_path = os.path.join(UPLOAD_FOLDER, photo.photo_path)
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                        print(f"Deleted: {photo_path}")
                except Exception as e:
                    return f"Error deleting file {photo.photo_path}: {e}",

            # Lösche das Foto aus der Datenbank
            db.session.delete(photo)

        db.session.commit()      
        return f"Deleted Photo", 200