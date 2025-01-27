from flask import Flask

from .api import api_v1_pb
from config import Config
from .auth import auth_pb
from .extensions import db, migrate, guard, cors, mail
from .models.user import User, TrustLevel, Role


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config_class)

    register_extensions(app)
    populate_db(app)

    # Register blueprints here
    app.register_blueprint(api_v1_pb, url_prefix='/api/v1')
    app.register_blueprint(auth_pb, url_prefix='/auth')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app


def register_extensions(app):
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    guard.init_app(app, User)
    cors.init_app(app)


def populate_db(app):
    with app.app_context():
        db.create_all()
        if Role.query.filter_by(name='User').first() is None:
            user_role = Role(name='User', description='A regular user')
            db.session.add(user_role)
        if Role.query.filter_by(name='Admin').first() is None:
            admin_role = Role(name='Admin', description='An administrator')
            db.session.add(admin_role)

        if TrustLevel.query.filter_by(name='Untrusted').first() is None:
            untrusted_level = TrustLevel(name='Untrusted', description='Untrusted users')
            db.session.add(untrusted_level)
        if TrustLevel.query.filter_by(name='Trusted').first() is None:
            trusted_level = TrustLevel(name='Trusted', description='Trusted users')
            db.session.add(trusted_level)
        db.session.commit()
