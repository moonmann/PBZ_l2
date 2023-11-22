from sqlalchemy import Column, Integer, String, create_engine, CheckConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()


class Drop(Base):
    __tablename__ = 'Drop'

    idDrop = Column(Integer, primary_key=True)
    drop_name = Column(String(100))
    diameter = Column(Integer)
    min_water_speed = Column(Integer)
    water_consuption = Column(Integer)
    angel_about_water = Column(Integer)
    distance_to_water = Column(Integer)
    distance_to_coast = Column(Integer)
    date = Column(String(100))


class Target(Base):
    __tablename__ = 'Target'

    idTarget = Column(Integer, primary_key=True)
    target_name = Column(String(100))
    drop_idDrop = Column(Integer, ForeignKey('Drop.idDrop'))
    Drop = relationship('Drop', backref='targets')


class WaterUseType(Base):
    __tablename__ = 'WaterUseType'

    idWaterUseType = Column(Integer, primary_key=True)
    water_use_type = Column(String(100))


class Factory(Base):
    __tablename__ = 'Factory'

    idFactory = Column(Integer, primary_key=True)
    factory_name = Column(String(100))
    waterUseType_idWaterUseType = Column(Integer, ForeignKey('WaterUseType.idWaterUseType'))
    target_idTarget = Column(Integer, ForeignKey('Target.idTarget'))
    WaterUseType = relationship('WaterUseType')
    Target = relationship('Target', backref='factories')


class Substance(Base):
    __tablename__ = 'Substance'

    idSubstance = Column(Integer, primary_key=True)
    danger_class = Column(Integer)
    lvf = Column(Integer)

    substance_name = Column(String(100))
    group = Column(Integer)


class WaterUseTypeToSubstance(Base):
    __tablename__ = 'WaterUseTypeToSubstance'

    idWaterUseTypeToSubstance = Column(Integer, primary_key=True)
    waterUseType_idWaterUseType = Column(Integer, ForeignKey('WaterUseType.idWaterUseType'))
    substance_idSubstance = Column(Integer, ForeignKey('Substance.idSubstance'))
    WaterUseType = relationship('WaterUseType')
    Substance = relationship('Substance')


class SubstanceToDrop(Base):
    __tablename__ = 'SubstanceToDrop'

    idSubstanceToDrop = Column(Integer, primary_key=True)
    concentration_in_drop = Column(Integer)
    concentration_in_target = Column(Integer)
    pdk = Column(Integer)
    knk = Column(Integer)
    substance_idSubstance = Column(Integer, ForeignKey('Substance.idSubstance'))
    drop_idDrop = Column(Integer, ForeignKey('Drop.idDrop'))
    Substance = relationship('Substance')
    Drop = relationship('Drop', backref='substances')


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
