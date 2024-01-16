from fastapi import APIRouter, Depends, Body, HTTPException
from typing import Union, Annotated
from sqlalchemy.orm import sessionmaker, Session
from starlette import status
from starlette.responses import JSONResponse

from config import settings
from sqlalchemy.ext.asyncio import create_async_engine

from models.Tags import Tags
from models.country import Base, Country
from models.models_answer.country import Country_answer

engine = create_async_engine(settings.POSTGRES_DATABASE_URLA, connect_args={"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


country_router = APIRouter(tags=[Tags.country],prefix="/country")

@country_router.get('/', response_model=Union[list[Country], None], tags=[Tags.country])
def get_countries(DB: Session = Depends(get_session)):
    countries = DB.query(Country).all()
    if countries == None:
        return JSONResponse(status_code=404, content={"message":"Нет записей"})
    return countries

@country_router.get('/{id}', response_model=Union[Country, None], tags=[Tags.country])
def get_country(id: int, DB: Session = Depends(get_session)):
    country = DB.query(Country).filter(Country.id == id).first()
    if country == None:
        return JSONResponse(status_code=404, content={"message":"Страна не найдена"})
    return country

@country_router.post('/', response_model=Union[Country, None], status_code=status.HTTP_201_CREATED, tags=[Tags.country])
def create_country(
        item: Annotated[Country, Body(embed=True, description="Новая запись")],
        DB: Session = Depends(get_session)):
    try:
        country = Country(id=item.id,
                          name = item.name,
                          square = item.square,
                          population = item.population,
                          form_of_government = item.form_of_government,
                          capital = item.capital,
                          percentage_of_urban_population = item.percentage_of_urban_population,
                          official_languages = item.official_languages,
                          head_of_state = item.head_of_state)
        if country is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(country)
        DB.commit()
        DB.refresh(country)
        return country
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошшла ошибка при добавлении объекта {country}")


@country_router.put('/', response_model=Union[Country, None], tags=[Tags.country])
def edit_country(item: Annotated[Country, Body(embed=True, description="Изменяем данные страны по id")], DB: Session = Depends(get_session)):
    country = DB.query(Country).filter(Country.id == item.id).first()
    if country == None:
        return JSONResponse(status_code=404, content={"message":"Страна не найдена"})
    country.name = item.name,
    country.square = item.square,
    country.population = item.population,
    country.form_of_government = item.form_of_government,
    country.capital = item.capital,
    country.percentage_of_urban_population = item.percentage_of_urban_population,
    country.official_languages = item.official_languages,
    country.head_of_state = item.head_of_state
    try:
        DB.commit()
        DB.refresh(country)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    return country


@country_router.delete('/{id}', response_model=Union[list[Country], None], tags=[Tags.country])
def delete_country(id: int, DB: Session = Depends(get_session)):
    country = DB.query(Country).filter(Country.id == id).first()
    if country == None:
        return JSONResponse(status_code=404, content={"message": "Страна не найдена"})
    try:
        DB.delete(country)
        DB.commit()
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": "Ошибка"})
    return JSONResponse(content={"message": f"Запись {id} удалена"})