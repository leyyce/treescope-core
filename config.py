import os

import pendulum

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32).hex())

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI') # 'postgresql://postgres:postgres@localhost:5432/treescope')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_LIFESPAN = os.environ.get('JWT_ACCESS_LIFESPAN', pendulum.duration(days=1))
    JWT_REFRESH_LIFESPAN = os.environ.get('JWT_REFRESH_LIFESPAN', pendulum.duration(days=30))
    JWT_PLACES = ['header']

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'treescope-core-mailer')
    MAIL_PORT = os.environ.get('MAIL_PORT', 1025)

    PRAETORIAN_CONFIRMATION_URI = os.environ.get('PRAETORIAN_CONFIRMATION_URI', 'http://localhost/auth/finalize')
    PRAETORIAN_CONFIRMATION_SUBJECT = os.environ.get('PRAETORIAN_CONFIRMATION_SUBJECT', 'Please confirm your registration for TreeScope')
    PRAETORIAN_CONFIRMATION_SENDER = os.environ.get('PRAETORIAN_CONFIRMATION_SENDER', 'no-reply@treescope.cs.hs-fulda.de')
    PRAETORIAN_CONFIRMATION_LIFESPAN = os.environ.get('PRAETORIAN_CONFIRMATION_LIFESPAN', pendulum.duration(days=1))

    PRAETORIAN_RESET_URI = os.environ.get('PRAETORIAN_RESET_URI', 'http://localhost/auth/reset-password')
    PRAETORIAN_RESET_SUBJECT = os.environ.get('PRAETORIAN_RESET_SUBJECT', 'TreeScope - Password Reset Request')
    PRAETORIAN_RESET_SENDER = os.environ.get('PRAETORIAN_RESET_SENDER', 'no-reply@treescope.cs.hs-fulda.de')
    PRAETORIAN_RESET_LIFESPAN = os.environ.get('PRAETORIAN_RESET_LIFESPAN', pendulum.duration(minutes=15))

    TREESCOPE_MAIL_CHANGE_URI = os.environ.get('TREESCOPE_MAIL_CHANGE_URI', 'http://localhost/auth/change-mail')
    TREESCOPE_MAIL_CHANGE_SUBJECT = os.environ.get('TREESCOPE_MAIL_CHANGE_SUBJECT', 'TreeScope - Mail Change Request')
    TREESCOPE_MAIL_CHANGE_SENDER = os.environ.get('TREESCOPE_MAIL_CHANGE_SENDER', 'no-reply@treescope.cs.hs-fulda.de')
    TREESCOPE_MAIL_CHANGE_LIFESPAN = os.environ.get('TREESCOPE_MAIL_CHANGE_LIFESPAN', pendulum.duration(minutes=15))