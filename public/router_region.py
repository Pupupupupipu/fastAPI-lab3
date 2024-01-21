from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Union, Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import JSONResponse

from config import settings
from db import engine


from models.region import Region
from models.models_answer.region import Region_answer

#engine = create_engine(settings.POSTGRES_DATABASE_URLA, connect_args={"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


region_router = APIRouter(tags=["region"], prefix="/api/region")

@region_router.get('/', response_model=Union[list[Region_answer], None])
def get_regions(DB: Session = Depends(get_session)):
    regions = DB.query(Region).all()
    if regions == None:
        return JSONResponse(status_code=404, content={"message":"Нет записей"})
    return regions

@region_router.get('/{id}', response_model=Union[Region_answer, None])
def get_region(id: int, DB: Session = Depends(get_session)):
    region = DB.query(Region).filter(Region.id_region == id).first()
    if region == None:
        return JSONResponse(status_code=404, content={"message":"Регион не найден"})
    return region

@region_router.post('/', response_model=Union[Region_answer, None], status_code=status.HTTP_201_CREATED)
def create_region(
        item: Annotated[Region_answer, Body(embed=True, description="Новая запись")],
        DB: Session = Depends(get_session)):
    try:
        region = Region(id_country = item.id_country,
                       name = item.name,
                       population = item.population,
                       percentage_of_urban_population = item.percentage_of_urban_population,
                       administrative_center = item.administrative_center)
        if region is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(region)
        DB.commit()
        DB.refresh(region)
        return region
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {region}")


@region_router.put('/', response_model=Union[Region_answer, None])
def edit_region(item: Annotated[Region_answer, Body(embed=True, description="Изменяем данные страны по id")], DB: Session = Depends(get_session)):
    region = DB.query(Region).filter(Region.id_region == item.id_region).first()
    if region == None:
        return JSONResponse(status_code=404, content={"message":"Регион не найден"})
    region.id_country = item.id_country,
    region.name = item.name,
    region.population = item.population,
    region.percentage_of_urban_population = item.percentage_of_urban_population,
    region.administrative_center = item.administrative_center
    try:
        DB.commit()
        DB.refresh(region)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    return region


@region_router.delete('/{id}', response_model=Union[list[Region_answer], None])
def delete_region(id: int, DB: Session = Depends(get_session)):
    region = DB.query(Region).filter(Region.id_region == id).first()
    if region == None:
        return JSONResponse(status_code=404, content={"message": "Регион не найден"})
    try:
        DB.delete(region)
        DB.commit()
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": "Ошибка"})
    return JSONResponse(content={"message": f"Запись {id} удалена"})

@region_router.patch('/{id}', response_model=Union[Region_answer, None])
def edit_region(item: Annotated[Region_answer, Body(embed=True, description="Изменяем данные региона по id")], DB: Session = Depends(get_session)):
    region = DB.query(Region).filter(Region.id_region== item.id_region).first()
    if region == None:
        return JSONResponse(status_code=404, content={"message":"Регион не найден"})
    if 0 != item.id_country:
        region.id_country = item.id_country
    if "string" != item.name:
        region.name = item.name
    if 0 != item.population:
        region.population = item.population
    if 0 != item.percentage_of_urban_population:
        region.percentage_of_urban_population = item.percentage_of_urban_population
    if "string" != item.administrative_center:
        region.administrative_center = item.administrative_center
    try:
        DB.commit()
        DB.refresh(region)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    return region