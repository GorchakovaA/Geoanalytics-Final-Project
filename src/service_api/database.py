from sqlalchemy import create_engine, Column, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/meteorites_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Meteorite(Base):
    __tablename__ = "meteorites"

    # Мы говорим SQLAlchemy: "в классе поле id, но в базе ищи колонку ogc_fid"
    id = Column("ogc_fid", Integer, primary_key=True)
    
    name = Column(String)
    recclass = Column(String)
    year = Column(String)
    mass = Column("mass (g)", String)
    reclat = Column(Float)
    reclong = Column(Float)
    # ВОЗВРАЩАЕМ ГЕОМЕТРИЮ
    geom = Column(Geometry("POINT"))
