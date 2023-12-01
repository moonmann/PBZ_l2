from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
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
    water_consumption = Column(Integer)
    angel_about_water = Column(Integer)
    distance_to_water = Column(Integer)
    distance_to_coast = Column(Integer)
    date = Column(String(100))


class Target(Base):
    __tablename__ = 'Target'

    idTarget = Column(Integer, primary_key=True)
    target_name = Column(String(100))
    drop_drop_name = Column(String(100), ForeignKey('Drop.drop_name'))
    Drop = relationship('Drop', backref='targets')


class WaterUseType(Base):
    __tablename__ = 'WaterUseType'

    idWaterUseType = Column(Integer, primary_key=True)
    water_use_type = Column(String(100))


class Factory(Base):
    __tablename__ = 'Factory'

    idFactory = Column(Integer, primary_key=True)
    factory_name = Column(String(100))
    waterUseType_water_use_type = Column(String(100), ForeignKey('WaterUseType.water_use_type'))
    target_target_name = Column(String(100), ForeignKey('Target.target_name'))
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
    waterUseType_water_use_type = Column(String(100), ForeignKey('WaterUseType.water_use_type'))
    substance_substance_name = Column(String(100), ForeignKey('Substance.substance_name'))
    WaterUseType = relationship('WaterUseType')
    Substance = relationship('Substance')


class SubstanceToDrop(Base):
    __tablename__ = 'SubstanceToDrop'

    idSubstanceToDrop = Column(Integer, primary_key=True)
    concentration_in_drop = Column(Integer)
    concentration_in_target = Column(Integer)
    pdk = Column(Integer)
    knk = Column(Integer)
    substance_substance_name = Column(String(100), ForeignKey('Substance.substance_name'))
    drop_drop_name = Column(String(100), ForeignKey('Drop.drop_name'))
    Substance = relationship('Substance')
    Drop = relationship('Drop', backref='substances')


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
