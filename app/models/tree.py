from decimal import Decimal

from app.extensions import db
from sqlalchemy import Float, ForeignKey, DECIMAL, DateTime, CheckConstraint, event, func
from sqlalchemy.orm import Mapped, mapped_column

class TreeType(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    scientific_name: Mapped[str] = mapped_column(unique=True, nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    a: Mapped[float] = mapped_column(nullable=True)
    b: Mapped[float] = mapped_column(nullable=True)
    c: Mapped[float] = mapped_column(nullable=True)
    d: Mapped[float] = mapped_column(nullable=True)
    e: Mapped[float] = mapped_column(nullable=True)
    f: Mapped[float] = mapped_column(nullable=True)
    g: Mapped[float] = mapped_column(nullable=True)

class Tree(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    initial_creator_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    tree_type_id: Mapped['int'] = mapped_column(ForeignKey('tree_type.id'), default=1, nullable=False)
    latitude: Mapped[Decimal] = mapped_column(DECIMAL(8, 6), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(DECIMAL(9, 6), nullable=False)
    # co2_stored: Mapped[Float] = mapped_column(DECIMAL(10, 2), default=0.00, nullable=False)
    health_status_id: Mapped[int] = mapped_column(ForeignKey('health_status.id'), default=1, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    tree_type: Mapped['TreeType'] = db.relationship(backref=db.backref('trees', lazy='dynamic'))
    measurements: Mapped[list['Measurement']] = db.relationship(back_populates='tree', lazy=True)
    health_status: Mapped['HealthStatus'] = db.relationship(back_populates='tree', lazy=True)
    files: Mapped[list['TreePhoto']] = db.relationship(back_populates='tree', lazy=True)

    '''
    __table_args__ = (
        CheckConstraint('co2_stored >= 0', name='check_co2_stored_positive'),
        CheckConstraint('environmental_impact >= 0', name='check_environmental_impact_positive'),
    )
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def co2_stored(self):
        co2_stored = None

        if self.tree_type.name in ['Amerikanische Birke', 'Gemeine Fichte', 'Waldkiefer']:
            avg_diameter = 0.
            for measurement in self.measurements:
                avg_diameter += measurement.trunk_diameter
            avg_diameter /= len(self.measurements)

            biomass = (
                    self.tree_type.a
                    + self.tree_type.b * avg_diameter
                    + self.tree_type.c * (avg_diameter**2)
                    + self.tree_type.d * (avg_diameter**3)
                    + self.tree_type.e * (avg_diameter**4)
                    + self.tree_type.f * (avg_diameter**5)
            )
            carbon_content = biomass * 0.5
            co2_stored = carbon_content * 3.67
        return co2_stored

# Event listener to set created_at and updated_at before insert
@event.listens_for(Tree, 'before_insert')
def set_created_at(mapper, connection, target):
    if target.created_at is None:
        target.created_at = func.now()
    if target.updated_at is None:
        target.updated_at = func.now()

# Event listener to set updated_at before update
@event.listens_for(Tree, 'before_update')
def set_updated_at(mapper, connection, target):
    target.updated_at = func.now()



class HealthStatus(db.Model):
    id: Mapped[int] = mapped_column( primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    tree: Mapped['Tree'] = db.relationship(back_populates='health_status')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)