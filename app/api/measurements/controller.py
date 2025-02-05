from flask import request
from app.api.measurements.dto import MeasurementDto
from flask_restx import Resource
from flask_praetorian import auth_required, current_user, auth_accepted, roles_required, PraetorianError

from app.api.measurements.service import MeasurementService
from app.api.measurements.utils import MeasurementSchema, TreePhotoSchema
from app.models.measurement import Measurement

ns = MeasurementDto.ns

measurement_schema = MeasurementSchema()
photo_schema = TreePhotoSchema(many=True)
   

@ns.route("/<int:tree_id>")
class Measurements(Resource):
    @ns.doc(
        'Get Measurements from a Tree',
        responses={
            200: 'Measurements send',
        },
    )
    @ns.marshal_list_with(MeasurementDto.measurement_with_files)
    def get(self, tree_id):
        """Returns all measurements for a given tree (sorted by newest first)"""
        return MeasurementService.get_measurements_from_tree(tree_id)
    
    @ns.doc(
        'Measurement creation',
        responses={
            201: 'Measurement created',
            400: 'Malformed data or validations failed.',
        },
        security='jwt_header',
    )
    @ns.expect(MeasurementDto.create_measurement_with_files)
    @auth_accepted
    def post(self, tree_id):
        """Create a measurement and with photos"""
        data = request.get_json()
        try:
            user = current_user()
            user_id = user.id
        except PraetorianError as e:
            user_id = None

        files = data.pop("files", [])
        
        if errors := measurement_schema.validate(data):
            return errors, 400
        message, code, measurement = MeasurementService.create_measurement(data, tree_id, user_id)
        if code != 201:
            ns.abort(code, message)
        message2, code = MeasurementService.create_photo(files, tree_id, user_id, measurement.id)
        if code != 201:
            ns.abort(code, message)
        return f"Created Measurement id {measurement.id}", code

@ns.route("/upload_photo/<int:measurement_id>")
class PhotoUpload(Resource):
    @ns.doc(
        'Measurement creation',
        responses={
            201: 'Measurement created',
            400: 'Malformed data or validations failed.',
        },
        security='jwt_header',
    )
    @ns.expect([MeasurementDto.tree_photo_create])
    @auth_accepted
    def post(self, measurement_id):
        """Add photo(s) to a measurement"""
        data = request.get_json()
        try:
            user = current_user()
            user_id = user.id
        except PraetorianError as e:
            user_id = None
        
        if errors := photo_schema.validate(data):
            return errors, 400
        measurement = Measurement.query.get(measurement_id)
        if not measurement:
            ns.abort(404, f"Measurement ID {measurement_id} not found")
        message, code = MeasurementService.create_photo(data, measurement.tree_id, user_id, measurement_id)
        if code != 201:
            ns.abort(code, message)
        return f"Uploaded photo(s)", code

@ns.route("/<int:measurement_id>")
class DeleteMeasurements(Resource):
    @ns.doc(
        'Measurement deletion',
        responses={
            200: 'Measurement deleted',
            401: 'Unauthorized',
            404: 'Measurement not found'
        },
        security='jwt_header',
    )
    @roles_required('Admin')
    def delete(self, measurement_id):
        """Deletes a measurement based on its ID"""
        message, code = MeasurementService.delete_photos(measurement_id)
        message, code = MeasurementService.delete_measurement(measurement_id)
        if code != 200:
            ns.abort(code, message)
        
        return f"Measurement {measurement_id} deleted successfully", 200