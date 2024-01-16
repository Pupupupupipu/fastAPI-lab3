from typing import Union, Annotated
from pydantic import Field
from models_old.User import User

class UserDB(User):
    password: Annotated[Union[str, None], Field(min_length = 4, max_length = 10)] = None