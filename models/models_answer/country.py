from typing import Union, Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column


class Country_answer(BaseModel):
    id_country: Union[int, None] = None
    name: Annotated[Union[str, None], Field(min_length = 3, max_length = 30)] = None
    square: Union[int, None] = None
    population: Union[int, None] = None
    form_of_government: Union[str, None] = None
    capital: Union[str, None] = None
    percentage_of_urban_population: Union[int, None] = None
    official_languages: Union[str, None] = None
    head_of_state: Union[str, None] = None



