from config.database import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, doc="Email Test")
    password = db.Column(db.String(120), nullable=False)
    roles = db.Column(db.String(120), default="user")  # Kommagetrennte Rollen

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def rolenames(self):
        """Die Rollen als Liste zurückgeben."""
        try:
            if self.roles is not None:
                return self.roles.split(",")
            else:
                return []
        except Exception as e:
            return [e]

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id
    

    def is_valid_password(self, password):
        return password == self.password
