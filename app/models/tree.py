from app.extensions import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DECIMAL, DateTime, CheckConstraint, event, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Tree(db.Model):
    __tablename__ = 'trees'

    id: Mapped[int] = mapped_column(primary_key=True)
    initial_creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    tree_type: Mapped[str] = mapped_column(String(128), nullable=True)
    latitude: Mapped[Float] = mapped_column(DECIMAL(8, 6), nullable=False)
    longitude: Mapped[Float] = mapped_column(DECIMAL(9, 6), nullable=False)
    co2_stored: Mapped[Float] = mapped_column(DECIMAL(10, 2), default=0.00, nullable=False)
    health_status: Mapped[int] = mapped_column(ForeignKey('healthstatuses.id'), default=1, nullable=False)
    environmental_impact: Mapped[Float] = mapped_column(DECIMAL(10, 2), default=0.00, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    measurements: Mapped[list['Measurement']] = db.relationship(back_populates='tree', lazy=True)
    health_status_info: Mapped['HealthStatus'] = db.relationship(back_populates='tree', lazy=True)
    files: Mapped[list['TreePhoto']] = db.relationship(back_populates='tree', lazy=True)


    __table_args__ = (
         CheckConstraint('co2_stored >= 0', name='check_co2_stored_positive'),
         CheckConstraint('environmental_impact >= 0', name='check_environmental_impact_positive'),
     )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Event listener to set created_at and updated_at before insert
@event.listens_for(Tree, 'before_insert')
def set_created_at(mapper, connection, target):
    if target.created_at is None:
        target.created_at = func.now()
    if target.updated_at is None:
        target.updated_at = func.now()


class HealthStatus(db.Model):
    __tablename__ = 'healthstatuses'

    id: Mapped[int] = mapped_column( primary_key=True)
    status: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    tree: Mapped['Tree'] = db.relationship(back_populates='health_status_info')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TreePhoto(db.Model):
    __tablename__ = 'treephotos'
    id: Mapped[int] = mapped_column(primary_key=True)
    tree_id: Mapped[int] = mapped_column(ForeignKey('trees.id'), nullable=False)
    measurement_id: Mapped[int] = mapped_column(ForeignKey('measurements.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    photopath: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    tree: Mapped['Tree'] = db.relationship(back_populates='files')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Event listener to set createdat before insert
@event.listens_for(TreePhoto, 'before_insert')
def set_createdat(mapper, connection, target):
    if target.created_at is None:
        target.created_at = func.now()
    