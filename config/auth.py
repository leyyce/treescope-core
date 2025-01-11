from flask_praetorian import Praetorian
from models.user import User

guard = Praetorian()

def init_guard(app):
    guard.init_app(app, User)
