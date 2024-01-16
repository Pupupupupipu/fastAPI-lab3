from typing import Union, Annotated
from pydantic import BaseModel, Field
from fastapi import Path


class User(BaseModel):
    id_user: Union[int, None] = None
    name: Annotated[Union[str, None], Field(min_length = 3, max_length = 10)] = None
    age: Annotated[Union[int, None], Path(ge=18, le=100)] = None