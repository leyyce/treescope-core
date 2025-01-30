import pendulum
from flask import current_app, make_response, render_template
from flask_praetorian import current_user
from flask_praetorian.constants import AccessType
from flask_praetorian.exceptions import AuthenticationError, PraetorianError, MissingClaimError

from app.auth.utils import ResetPasswordForm
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
        email = data['email'].lower()
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
    def send_verification_mail(data):
        success_response = {
            'message': 'If a user with the given mail address exists, a verification mail will be send shortly.'
        }

        email = data['email'].lower()

        user = User.query.filter_by(email=email).first()

        if user is None:
            return success_response, 200
        if user.is_valid():
            return 'Mail address was already verified.', 403
        guard.send_registration_email(email, user=user)
        return success_response, 200

    @staticmethod
    def finalize_registration(token):
        try:
            user = guard.get_user_from_registration_token(token)
            user.verified = True
            db.session.commit()
            return make_response(render_template("auth/finalize_success.html",
                                                 name = user.first_name if user.first_name else user.username,
                                                 addr = user.email,
                                                 title="Verification success - TreeScope"
                                                 )
                                 )
        except PraetorianError as e:
            return make_response(render_template("auth/finalize_error.html",
                                                 error=e.message,
                                                 title="Verification failed - TreeScope"
                                                 )
                                 )

    @staticmethod
    def change_mail(token):
        try:
            user = guard.get_user_from_registration_token(token)
            data = guard.extract_jwt_token(token, access_type=AccessType.register)
            MissingClaimError.require_condition(
                "custom_claims" in data,
                "Token is missing custom_claims",
            )
            custom_claims = data['custom_claims']
            MissingClaimError.require_condition(
                "new_mail_address" in custom_claims,
                "Token is missing new_mail_address custom claim",
            )
            new_mail_address = custom_claims['new_mail_address'].lower()
            if User.query.filter_by(email=new_mail_address).first() is not None:
                return make_response(render_template("auth/mail_change_error.html",
                                                     error=f'The mail address {new_mail_address} is already in use.',
                                                     title="Mail change failed - TreeScope"
                                                     )
                                     )
            user.email = new_mail_address
            db.session.commit()
            return make_response(render_template("auth/mail_change_success.html",
                                                 name=user.first_name if user.first_name else user.username,
                                                 addr=user.email,
                                                 title="Mail change success - TreeScope"
                                                 )
                                 )
        except PraetorianError as e:
            return make_response(render_template("auth/mail_change_error.html",
                                                 error=e.message,
                                                 title="Mail change failed - TreeScope"
                                                 )
                                 )

    @staticmethod
    def request_mail_change(data):
        email = data['email'].lower()
        password = data['password']

        user = current_user()

        # Check if the email is taken
        if User.query.filter_by(email=email).first() is not None:
            return 'Email is already being used.', 403

        guard.authenticate(user.username, password)

        mail_change_token = guard.encode_jwt_token(
            user,
            override_access_lifespan=current_app.config.get('TREESCOPE_MAIL_CHANGE_LIFESPAN'),
            is_registration_token=True,
            custom_claims={
                'new_mail_address': email,
            }
        )

        with open('app/templates/mail/mail_change_email.html') as fh:
            template = fh.read()

        guard.send_token_email(
            email,
            template=template,
            action_sender=current_app.config.get('TREESCOPE_MAIL_CHANGE_SENDER'),
            action_uri=current_app.config.get('TREESCOPE_MAIL_CHANGE_URI'),
            subject=current_app.config.get('TREESCOPE_MAIL_CHANGE_SUBJECT'),
            custom_token=mail_change_token)

        return {'message': f'Verification mail to {email} will be send shortly.'}, 200

    @staticmethod
    def change_password(data):
        old_password = data['old_password']
        new_password = data['new_password']

        user = current_user()
        try:
            guard.authenticate(user.username, old_password)
            user.password = new_password
            db.session.commit()
            return {'message': 'Password changed successfully.'}, 200
        except AuthenticationError:
            return 'Old password is wrong', 401

    @staticmethod
    def send_reset_mail(data):
        success_response = {
            'message': 'If a user with the given mail address exists, a password reset mail will be send shortly.'
        }

        email = data['email'].lower()
        user = User.query.filter_by(email=email).first()

        if user is None:
            return success_response, 200
        if not user.is_valid():
            return "Email address not verified. Verify the address first before requesting a password change", 403
        guard.send_reset_email(email, user=user)
        return success_response, 200

    @staticmethod
    def reset_password(token):
        try:
            user = guard.validate_reset_token(token)
            form = ResetPasswordForm()
            if form.validate_on_submit():
                user.password = form.password.data
                db.session.commit()
                return make_response(render_template("auth/reset_password_success.html",
                                                     name=user.first_name if user.first_name else user.username,
                                                     addr=user.email,
                                                     title="Pasword reset success - TreeScope"
                                                     )
                                     )
            return make_response(render_template("auth/reset_password.html",
                                                 title="Reset password - TreeScope",
                                                 form=form
                                                 )
                                 )
        except PraetorianError as e:
            return make_response(render_template("auth/reset_password_error.html",
                                                 error=e.message,
                                                 title="Password reset failed - TreeScope"
                                                 )
                                 )