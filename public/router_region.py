from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Union, Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from db import get_session

from models.region import Region
from models.models_answer.region import Region_answer




region_router = APIRouter(tags=["region"], prefix="/api/region")

@region_router.get('/', response_model=Union[list[Region_answer], None])
async def get_regions(DB: AsyncSession = Depends(get_session)):
    regions = await DB.execute(select(Region))
    if regions == None:
        return JSONResponse(status_code=404, content={"message":"Нет записей"})
    return regions.scalars().all()

@region_router.get('/{id}', response_model=Union[Region_answer, None])
async def get_region(id: int, DB: AsyncSession = Depends(get_session)):
    region = await DB.execute(select(Region).filter(Region.id_region == id))
    if region == None:
        return JSONResponse(status_code=404, content={"message":"Регион не найден"})
    return region.scalars().first()

@region_router.post('/', response_model=Union[Region_answer, None], status_code=status.HTTP_201_CREATED)
async def create_region(
        item: Annotated[Region_answer, Body(embed=True, description="Новая запись")],
        DB: AsyncSession = Depends(get_session)):
    try:
        region = Region(id_country = item.id_country,
                       name = item.name,
                       population = item.population,
                       percentage_of_urban_population = item.percentage_of_urban_population,
                       administrative_center = item.administrative_center)
        if region is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(region)
        await DB.commit()
        await DB.refresh(region)
        return region
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {region}")


@region_router.put('/', response_model=Union[Region_answer, None])
async def edit_region(item: Annotated[Region_answer, Body(embed=True, description="Изменяем данные страны по id")], DB: AsyncSession = Depends(get_session)):
    region = await DB.execute(select(Region).where(Region.id_region == item.id_region))
    region = region.scalars().first()
    if region == None:
        return JSONResponse(status_code=404, content={"message":"Регион не найден"})
    region.name = item.name
    region.population = item.population
    region.percentage_of_urban_population = item.percentage_of_urban_population
    region.administrative_center = item.administrative_center
    try:
        await DB.commit()
        await DB.refresh(region)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    return region


@region_router.delete('/{id}', response_model=Union[list[Region_answer], None])
async def delete_region(id: int, DB: AsyncSession = Depends(get_session)):
    region = await DB.execute(select(Region).where(Region.id_region == id))
    region = region.scalars().first()
    if region == None:
        return JSONResponse(status_code=404, content={"message": "Регион не найден"})
    try:
        await DB.delete(region)
        await DB.commit()
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": "Ошибка"})
    return JSONResponse(content={"message": f"Запись {id} удалена"})

@region_router.patch('/{id}', response_model=Union[Region_answer, None])
async def edit_region(item: Annotated[Region_answer, Body(embed=True, description="Изменяем данные региона по id")], DB: AsyncSession = Depends(get_session)):
    region = await DB.execute(select(Region).where(Region.id_region == item.id_region))
    region = region.scalars().first()
    if region == None:
        return JSONResponse(status_code=404, content={"message":"Регион не найден"})
    if "string" != item.name:
        region.name = item.name
    if 0 != item.population:
        region.population = item.population
    if 0 != item.percentage_of_urban_population:
        region.percentage_of_urban_population = item.percentage_of_urban_population
    if "string" != item.administrative_center:
        region.administrative_center = item.administrative_center
    try:
        await DB.commit()
        await DB.refresh(region)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    return region