from sqlalchemy import Column, Integer, String, ForeignKey, Identity
from sqlalchemy.orm import declarative_base

from models.country import Country
from models.region import Region

Base = declarative_base()

class City(Base):
    __tablename__ = "city"
    id_city = Column(Integer,Identity(start=4), primary_key=True)
    id_country = Column(Integer, ForeignKey(Country.id_country))
    id_region = Column(Integer, ForeignKey(Region.id_region))
    name = Column(String, nullable=False)
    geographical_coordinates = Column(String, nullable=False)
    population = Column(Integer, nullable=False)

