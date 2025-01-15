from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, DECIMAL, event, func
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db, guard
from flask_praetorian.user_mixins import SQLAlchemyUserMixin

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


class Role(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)


class TrustLevel(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)


class User(db.Model, SQLAlchemyUserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    trust_level: Mapped[int] = mapped_column(ForeignKey('trust_level.id'), default=1, nullable=False)
    roles = db.relationship('Role', secondary=user_roles, lazy='dynamic', backref=db.backref('users', lazy='dynamic'))
    xp: Mapped[int] = mapped_column(default=0, nullable=False)
    latitude: Mapped[Decimal] = mapped_column(DECIMAL(8, 6), nullable=True)
    longitude: Mapped[Decimal] = mapped_column(DECIMAL(9, 6), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        CheckConstraint('xp >= 0', name='check_xp_positive'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_role = Role.query.filter_by(name='User').first()
        if default_role:
            self.roles.append(default_role)

    @property
    def rolenames(self):
        return [role.name for role in self.roles]

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, value):
        self.hashed_password = guard.hash_password(value)


# Event listener to set created_at and updated_at before insert
@event.listens_for(User, 'before_insert')
def set_created_at(mapper, connection, target):
    if target.created_at is None:
        target.created_at = func.now()
    if target.updated_at is None:
        target.updated_at = func.now()


# Event listener to set updated_at before update
@event.listens_for(User, 'before_update')
def set_updated_at(mapper, connection, target):
    target.updated_at = func.now()
