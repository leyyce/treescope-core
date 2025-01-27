
from app.extensions import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DECIMAL, DateTime, CheckConstraint, event, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Measurement(db.Model):
    __tablename__ = 'measurements'

    id: Mapped[int] = mapped_column(primary_key=True)
    tree_id: Mapped[int] = mapped_column(ForeignKey('trees.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    suspected_tree_type: Mapped[str] = mapped_column(String(128), nullable=True)
    height: Mapped[Float] = mapped_column(DECIMAL(5, 2), nullable=False)
    inclination: Mapped[int] = mapped_column(Integer, nullable=False)
    trunk_diameter: Mapped[Float] = mapped_column(DECIMAL(5, 2), nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    tree: Mapped['Tree'] = db.relationship(back_populates='measurements')

    __table_args__ = (
        CheckConstraint('height > 0', name='check_height_positive'),
        CheckConstraint('inclination >= 0 AND inclination <= 90', name='check_inclination_valid'),
        CheckConstraint('trunk_diameter > 0', name='check_trunk_diameter_positive'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Event listener to set createdat before insert
@event.listens_for(Measurement, 'before_insert')
def set_createdat(mapper, connection, target):
    if target.created_at is None:
        target.created_at = func.now()
