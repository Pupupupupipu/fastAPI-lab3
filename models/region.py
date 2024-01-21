from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from models.country import Country

Base = declarative_base()

class Region(Base):
    __tablename__ = "region"
    id_region = Column(Integer, primary_key=True)
    id_country = Column(Integer, ForeignKey(Country.id_country))
    name = Column(String, index=True, nullable=False)
    population = Column(Integer)
    percentage_of_urban_population = Column(Integer)
    administrative_center = Column(String, nullable=False)

