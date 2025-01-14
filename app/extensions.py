from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_praetorian import Praetorian

db = SQLAlchemy()
migrate = Migrate()
guard = Praetorian()
