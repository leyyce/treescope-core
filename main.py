from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from config.database import db
from config.auth import guard, init_guard
from models.user import User
from routes.user_routes import user_namespace

app = Flask(__name__)
app.config.from_object("config.settings.Config")

# Datenbank initialisieren
db.init_app(app)
#migrate = Migrate(app, db)

# Guard initialisieren
init_guard(app)

# API initialisieren
api = Api(app, doc="/api/docs", title="User Management API", version="1.0")

# Namespace registrieren
api.add_namespace(user_namespace, path="/api/users")

if __name__ == "__main__":
    app.run(debug=True)
