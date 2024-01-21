from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Union, Annotated


from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import JSONResponse

from db import engine


from models.city import City
from models.models_answer.city import City_answer


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


city_router = APIRouter(tags=["city"], prefix="/api/city")

@city_router.get('/', response_model=Union[list[City_answer], None])
def get_cities(DB: Session = Depends(get_session)):
    cities = DB.query(City).all()
    if cities == None:
        return JSONResponse(status_code=404, content={"message":"Нет записей"})
    return cities

@city_router.get('/{id}', response_model=Union[City_answer, None])
def get_city(id: int, DB: Session = Depends(get_session)):
    city = DB.query(City).filter(City.id_city == id).first()
    if city == None:
        return JSONResponse(status_code=404, content={"message":"Город не найден"})
    return city

@city_router.post('/', response_model=Union[City_answer, None], status_code=status.HTTP_201_CREATED)
def create_city(
        item: Annotated[City_answer, Body(embed=True, description="Новая запись")],
        DB: Session = Depends(get_session)):
    try:
        city = City(id_country = item.id_country,
                    id_region = item.id_region,
                    name = item.name,
                    geographical_coordinates = item.geographical_coordinates,
                    population = item.population)
        if city is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(city)
        DB.commit()
        DB.refresh(city)
        return city
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {city}")


@city_router.put('/', response_model=Union[City_answer, None])
def edit_city(item: Annotated[City_answer, Body(embed=True, description="Изменяем данные страны по id")], DB: Session = Depends(get_session)):
    city = DB.query(City).filter(City.id_city == item.id_city).first()
    if city == None:
        return JSONResponse(status_code=404, content={"message":"Город не найден"})
    city.id_country = item.id_country,
    city.id_region = item.id_region,
    city.name = item.name,
    city.geographical_coordinates = item.geographical_coordinates,
    city.population = item.population
    try:
        DB.commit()
        DB.refresh(city)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    return city


@city_router.delete('/{id}', response_model=Union[list[City_answer], None])
def delete_city(id: int, DB: Session = Depends(get_session)):
    city = DB.query(City).filter(City.id_city == id).first()
    if city == None:
        return JSONResponse(status_code=404, content={"message": "Город не найден"})
    try:
        DB.delete(city)
        DB.commit()
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": "Ошибка"})
    return JSONResponse(content={"message": f"Запись {id} удалена"})

@city_router.patch('/{id}', response_model=Union[City_answer, None])
def edit_city(item: Annotated[City_answer, Body(embed=True, description="Изменяем данные города по id")], DB: Session = Depends(get_session)):
    city = DB.query(City).filter(City.id_city == item.id_city).first()
    if city == None:
        return JSONResponse(status_code=404, content={"message":"Город не найден"})
    if 0 != item.id_country:
        city.id_country = item.id_country
    if 0 != item.id_region:
        city.id_region = item.id_region
    if "string" != item.name:
        city.name = item.name
    if "string" != item.geographical_coordinates:
        city.geographical_coordinates = item.geographical_coordinates
    if 0 != item.population:
        city.population = item.population
    try:
        DB.commit()
        DB.refresh(city)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    return city