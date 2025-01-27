from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_praetorian import Praetorian
from flask_cors import CORS
from flask_mailman import Mail

db = SQLAlchemy()
migrate = Migrate()
guard = Praetorian()
cors = CORS()
mail = Mail()
