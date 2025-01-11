from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from config.database import db
from routes.user_routes import user_blueprint

app = Flask(__name__)
app.config.from_object("config.settings.Config")

# Datenbank initialisieren
db.init_app(app)
migrate = Migrate(app, db)

# API und Routen registrieren
api = Api(app, doc="/api/docs", title="User Management API", version="1.0")
app.register_blueprint(user_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
