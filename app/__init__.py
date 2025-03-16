from flask import Flask

from .api import api_v1_pb
from config import Config
from .auth import auth_pb
from .extensions import db, migrate, guard, cors, mail
from .models.user import User, TrustLevel, Role
from .models.tree import Tree, HealthStatus, TreeType
from .models.measurement import Measurement, TreePhoto


def create_app(config_class=Config):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(config_class)

    register_extensions(app)
    populate_db(app)

    # Register blueprints here
    app.register_blueprint(api_v1_pb, url_prefix='/api/v1')
    app.register_blueprint(auth_pb, url_prefix='/auth')

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

        # User roles
        if Role.query.filter_by(name='User').first() is None:
            user_role = Role(name='User', description='Benutzerkonto mit Standartrechten')
            db.session.add(user_role)
        if Role.query.filter_by(name='Admin').first() is None:
            admin_role = Role(name='Admin', description='Administratorkonto mit erweiterten Rechten')
            db.session.add(admin_role)

        # Trust level
        if TrustLevel.query.filter_by(name='Untrusted').first() is None:
            untrusted_level = TrustLevel(name='Untrusted', description='Nicht vertrauenswürdiger Benutzer')
            db.session.add(untrusted_level)
        if TrustLevel.query.filter_by(name='Trusted').first() is None:
            trusted_level = TrustLevel(name='Trusted', description='Vertrauenswürdiger Benutzer')
            db.session.add(trusted_level)

        # Health status
        if HealthStatus.query.filter_by(name='Unbekannt').first() is None:
            h_status = HealthStatus(name='Unbekannt', description='Gesundheitszustand nicht bekannt')
            db.session.add(h_status)
        if HealthStatus.query.filter_by(name='Gesund').first() is None:
            h_status = HealthStatus(name='Gesund', description='Baum ist gesund')
            db.session.add(h_status)
        if HealthStatus.query.filter_by(name='Beeinträchtigt').first() is None:
            h_status = HealthStatus(name='Beeinträchtigt', description='Gesundheit des Baums beeinträchtigt')
            db.session.add(h_status)

        # Tree type
        if TreeType.query.filter_by(name='Unbekannt').first() is None:
            tree_type = TreeType(name='Unbekannt', description='Baumart ist nicht bekannt')
            db.session.add(tree_type)
        if TreeType.query.filter_by(name='Andere').first() is None:
            tree_type = TreeType(name='Andere', description='Baumart ist nicht gelistet')
            db.session.add(tree_type)
        if TreeType.query.filter_by(name='Amerikanische Birke').first() is None:
            tree_type = TreeType(
                name='Amerikanische Birke',
                description='Amerikanische Birke',
                scientific_name='Betula alleghaniensis',
                a=0.8,
                b=-1.0119,
                c=0.4244,
                d=0.0075,
                e=-4e-5,
                f=1e-7
            )
            db.session.add(tree_type)
        if TreeType.query.filter_by(name='Gemeine Fichte').first() is None:
            tree_type = TreeType(
                name='Gemeine Fichte',
                description='Gemeine Fichte',
                scientific_name='Picea abies',
                a=10,
                b=-1.3638,
                c=0.4216,
                d=0.0041,
                e=-3e-5,
                f=1e-7
            )
            db.session.add(tree_type)
        if TreeType.query.filter_by(name='Waldkiefer').first() is None:
            tree_type = TreeType(
                name='Waldkiefer',
                description='Waldkiefer',
                scientific_name='Pinus sylvestris',
                a=1.5,
                b=-0.8569,
                c=0.3074,
                d=0.003,
                e=-3e-5,
                f=1e-7
            )
            db.session.add(tree_type)
        db.session.commit()
