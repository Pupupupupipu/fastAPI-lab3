from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = "country"
    id_country = Column(Integer, Identity(start=4), primary_key=True)
    name = Column(String, index=True, nullable=False)
    square = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)
    form_of_government = Column(String, nullable=False)
    capital = Column(String, nullable=False)
    percentage_of_urban_population = Column(Integer, nullable=False)
    official_languages = Column(String, nullable=False)
    head_of_state = Column(String, nullable=False)

