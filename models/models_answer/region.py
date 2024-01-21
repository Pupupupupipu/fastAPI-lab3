from typing import Union, Annotated
from pydantic import BaseModel, Field


class Region_answer(BaseModel):
    id_country: Union[int, None] = None
    id_region: Union[int, None] = None
    name: Annotated[Union[str, None], Field(min_length = 3, max_length = 30)] = None
    population: Union[int, None] = None
    percentage_of_urban_population: Union[int, None] = None
    administrative_center: Union[str, None] = None



