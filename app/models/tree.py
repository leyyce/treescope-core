from app.extensions import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DECIMAL, DateTime, CheckConstraint, event, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Tree(db.Model):
    __tablename__ = 'trees'

    id: Mapped[int] = mapped_column(primary_key=True)
    initialcreatorid: Mapped[int] = mapped_column(ForeignKey('user.id'))
    treetype: Mapped[str] = mapped_column(String(128), nullable=True)
    latitude: Mapped[Float] = mapped_column(DECIMAL(8, 6), nullable=False)
    longitude: Mapped[Float] = mapped_column(DECIMAL(9, 6), nullable=False)
    co2stored: Mapped[Float] = mapped_column(DECIMAL(10, 2), default=0.00, nullable=False)
    healthstatus: Mapped[int] = mapped_column(ForeignKey('healthstatuses.id'), default=1, nullable=False)
    environmentalimpact: Mapped[Float] = mapped_column(DECIMAL(10, 2), default=0.00, nullable=False)
    createdat: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    measurements: Mapped[list['Measurement']] = db.relationship(back_populates='tree', lazy=True)
    healthstatusinfo: Mapped['HealthStatus'] = db.relationship(back_populates='tree', lazy=True)
    files: Mapped[list['TreePhoto']] = db.relationship(back_populates='tree', lazy=True)


    __table_args__ = (
         CheckConstraint('co2stored >= 0', name='check_co2_stored_positive'),
         CheckConstraint('environmentalimpact >= 0', name='check_environmental_impact_positive'),
     )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Event listener to set createdat before insert
@event.listens_for(Tree, 'before_insert')
def set_createdat(mapper, connection, target):
    if target.createdat is None:
        target.createdat = func.now()


class HealthStatus(db.Model):
    __tablename__ = 'healthstatuses'

    id: Mapped[int] = mapped_column( primary_key=True)
    status: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    tree: Mapped['Tree'] = db.relationship(back_populates='healthstatusinfo')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TreePhoto(db.Model):
    __tablename__ = 'treephotos'
    id: Mapped[int] = mapped_column(primary_key=True)
    treeid: Mapped[int] = mapped_column(ForeignKey('trees.id'), nullable=False)
    measurementid: Mapped[int] = mapped_column(ForeignKey('measurements.id'), nullable=False)
    userid: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    photopath: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    uploadedat: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    tree: Mapped['Tree'] = db.relationship(back_populates='files')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Event listener to set createdat before insert
@event.listens_for(TreePhoto, 'before_insert')
def set_createdat(mapper, connection, target):
    if target.uploadedat is None:
        target.uploadedat = func.now()
    