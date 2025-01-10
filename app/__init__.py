from flask import Flask

from .apis import api_v1_pb
from config import Config
from .extensions import db, migrate
from .models.user import User, TrustLevel, AccountType

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)

    # Register blueprints here
    app.register_blueprint(api_v1_pb, url_prefix='/api/v1')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
