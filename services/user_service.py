from models.user import User
from config.database import db
from config.auth import guard


def create_user(username, email, password, roles):
    user = User(username=username, email=email, password=guard.hash_password(password), roles=roles)
    db.session.add(user)
    db.session.commit() 
    return user

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_all_users():
    return User.query.all()

def update_user(user_id, username=None, email=None):
    user = User.query.get(user_id)
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user


