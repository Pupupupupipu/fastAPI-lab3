from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class City(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True)
    id_country = Column(Integer, ForeignKey("country.id"))
    id_region = Column(Integer, ForeignKey("region.id"))
    name = Column(String, index=True, nullable=False)
    geographical_coordinates = Column(String)
    population = Column(Integer)

