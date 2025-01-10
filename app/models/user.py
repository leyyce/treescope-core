from sqlalchemy import CheckConstraint, DateTime, ForeignKey, CHAR, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db

class AccountType(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

class TrustLevel(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    salt: Mapped[str] = mapped_column(CHAR(256), nullable=False)
    verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    trust_level: Mapped[int] = mapped_column(ForeignKey("trust_level.id"), default=1, nullable=False)
    account_type: Mapped[int] = mapped_column(ForeignKey("account_type.id"), default=1, nullable=False)
    xp: Mapped[int] = mapped_column(default=0, nullable=False)
    latitude: Mapped[float] = mapped_column(DECIMAL(8, 6), nullable=True)
    longitude: Mapped[float] = mapped_column(DECIMAL(8, 6), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default='now()', nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default='now()', onupdate='now()', nullable=False)

    __table_args__ = (
        CheckConstraint('xp >= 0', name='check_xp_positive'),
        CheckConstraint('length(salt) = 256', name='check_salt_length'),
    )
