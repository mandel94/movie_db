from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, Float, Date
from .base import Base
from engine import engine



class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    regia = Column(String, nullable=False)
    genere = Column(String, nullable=False)



Base.metadata.create_all(engine)

