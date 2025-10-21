from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Empleado(Base):
    __tablename__ = "empleados"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    cargo = Column(String)
    sueldo_base = Column(Float)
    horas_extras = Column(Integer)
    valor_hora_extra = Column(Float)
    presentismo = Column(Boolean)
    neto = Column(Float)

def get_engine():
    return create_engine("sqlite:///empleados.db")

def create_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
