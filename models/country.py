from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    square = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)
    form_of_government = Column(String, nullable=False)
    capital = Column(String, nullable=False)
    percentage_of_urban_population = Column(Integer, nullable=False)
    official_languages = Column(String, nullable=False)
    head_of_state = Column(String, nullable=False)

