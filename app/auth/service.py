from flask_praetorian.exceptions import AuthenticationError

from app.models.user import User
from app.extensions import db, guard


class AuthService:
    @staticmethod
    def login(data):
        # Assign vars
        username = data['username']
        password = data['password']

        try:
            user = guard.authenticate(username, password)
            if user.is_valid():
                resp = {
                    'access_token': guard.encode_jwt_token(user),
                    'user': user,
                }
                return resp, 200
            return "Email address not verified.", 403
        except AuthenticationError as e:
            return e.message, 401

    @staticmethod
    def register(data):
        # Assign vars

        ## Required values
        email = data['email']
        username = data['username']
        password = data['password']

        # Check if the email is taken
        if User.query.filter_by(email=email).first() is not None:
            return 'Email is already being used.', 403

        # Check if the username is taken
        if User.query.filter_by(username=username).first() is not None:
            return 'Username is already taken.', 403

        ## Optional
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        longitude = data.get('longitude')
        latitude = data.get('latitude')

        new_user = User(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            longitude=longitude,
            latitude=latitude,
        )

        db.session.add(new_user)
        db.session.flush()

        # Commit changes to DB
        db.session.commit()

        guard.send_registration_email(email, user=new_user)

        return new_user, 201

    @staticmethod
    def send_validation_mail(data):
        success_response = {
            'message': 'If a user with the given mail address exists, a verification mail will be send shortly.'
        }

        email = data['email']

        user = User.query.filter_by(email=email).first()

        if user is None:
            return success_response, 200
        if user.is_valid():
            return 'Mail address was already verified.', 403
        guard.send_registration_email(email, user=user)
        return success_response, 200