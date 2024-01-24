from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Union, Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from db import get_session

from models.city import City
from models.models_answer.city import City_answer


city_router = APIRouter(tags=["city"], prefix="/api/city")

@city_router.get('/', response_model=Union[list[City_answer], None])
async def get_cities(DB: AsyncSession = Depends(get_session)):
    cities = await DB.execute(select(City))
    if cities == None:
        return JSONResponse(status_code=404, content={"message":"Нет записей"})
    return cities.scalars().all()

@city_router.get('/{id}', response_model=Union[City_answer, None])
async def get_city(id: int, DB: AsyncSession = Depends(get_session)):
    city = await DB.execute(select(City).filter(City.id_city == id))
    if city == None:
        return JSONResponse(status_code=404, content={"message":"Город не найден"})
    return city.scalars().first()

@city_router.post('/', response_model=Union[City_answer, None], status_code=status.HTTP_201_CREATED)
async def create_city(
        item: Annotated[City_answer, Body(embed=True, description="Новая запись")],
        DB: AsyncSession = Depends(get_session)):
    try:
        city = City(id_country = item.id_country,
                    id_region = item.id_region,
                    name = item.name,
                    geographical_coordinates = item.geographical_coordinates,
                    population = item.population)
        if city is None:
            return HTTPException(status_code=404, detail="Объект не определен")
        DB.add(city)
        await DB.commit()
        await DB.refresh(city)
        return city
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {city}")


@city_router.put('/', response_model=Union[City_answer, None])
async def edit_city(item: Annotated[City_answer, Body(embed=True, description="Изменяем данные страны по id")], DB: AsyncSession = Depends(get_session)):
    city = await DB.execute(select(City).where(City.id_city == item.id_city))
    city = city.scalars().first()
    if city is None:
        return JSONResponse(status_code=404, content={"message":"Город не найден"})
    city.name = item.name
    city.geographical_coordinates = item.geographical_coordinates
    city.population = item.population
    try:
        await DB.commit()
        await DB.refresh(city)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    return city


@city_router.delete('/{id}', response_model=Union[list[City_answer], None])
async def delete_city(id: int, DB: AsyncSession = Depends(get_session)):
    city = await DB.execute(select(City).where(City.id_city == id))
    city = city.scalars().first()
    if city == None:
        return JSONResponse(status_code=404, content={"message": "Город не найден"})
    try:
        await DB.delete(city)
        await DB.commit()
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": "Ошибка"})
    return JSONResponse(content={"message": f"Запись {id} удалена"})

@city_router.patch('/{id}', response_model=Union[City_answer, None])
async def edit_city(item: Annotated[City_answer, Body(embed=True, description="Изменяем данные города по id")], DB: AsyncSession = Depends(get_session)):
    city = await DB.execute(select(City).where(City.id_city == item.id_city))
    city = city.scalars().first()
    if city == None:
        return JSONResponse(status_code=404, content={"message":"Город не найден"})
    if "string" != item.name:
        city.name = item.name
    if "string" != item.geographical_coordinates:
        city.geographical_coordinates = item.geographical_coordinates
    if 0 != item.population:
        city.population = item.population
    try:
        await DB.commit()
        await DB.refresh(city)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    return city