from typing import Union, Annotated
from pydantic import BaseModel, Field


class City_answer(BaseModel):
    id_city: Union[int, None] = None
    id_country: Union[int, None] = None
    id_region: Union[int, None] = None
    name: Annotated[Union[str, None], Field(min_length = 3, max_length = 30)] = None
    geographical_coordinates: Union[str, None] = None
    population: Union[int, None] = None



