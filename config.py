import os

import pendulum

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32).hex())
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/treescope')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_LIFESPAN = os.environ.get('JWT_ACCESS_LIFESPAN', pendulum.duration(hours=24))
    JWT_REFRESH_LIFESPAN = os.environ.get('JWT_REFRESH_LIFESPAN', pendulum.duration(days=30))
    JWT_PLACES = ['header']
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'mailer')
    MAIL_PORT = os.environ.get('MAIL_PORT', 1025)
    PRAETORIAN_CONFIRMATION_SENDER = os.environ.get('PRAETORIAN_CONFIRMATION_SENDER', 'no-reply@treescope.cs.hs-fulda.de')
    PRAETORIAN_CONFIRMATION_URI = os.environ.get('PRAETORIAN_CONFIRMATION_URI', 'http://localhost:5000/auth/finalize')
