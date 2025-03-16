
from app.extensions import db
from sqlalchemy import Integer, ForeignKey, DateTime, CheckConstraint, event, func
from sqlalchemy.orm import Mapped, mapped_column


class Measurement(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    tree_id: Mapped[int] = mapped_column(ForeignKey('tree.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    height: Mapped[float] = mapped_column(nullable=False)
    inclination: Mapped[int] = mapped_column(Integer, nullable=False)
    trunk_diameter: Mapped[float] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    files: Mapped[list['TreePhoto']] = db.relationship(back_populates='measurements', lazy=True)
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
def set_created_at(mapper, connection, target):
    if target.created_at is None:
        target.created_at = func.now()


class TreePhoto(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    tree_id: Mapped[int] = mapped_column(ForeignKey('tree.id'), nullable=False)
    measurement_id: Mapped[int] = mapped_column(ForeignKey('measurement.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    photo_path: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    measurements: Mapped['Measurement'] = db.relationship(back_populates='files')
    tree: Mapped['Tree'] = db.relationship(back_populates='files')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Event listener to set created_at before insert
@event.listens_for(TreePhoto, 'before_insert')
def set_created_at(mapper, connection, target):
    if target.created_at is None:
        target.created_at = func.now()