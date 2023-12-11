from typing import Union
from models.UserDB import UserDB

class Admin(UserDB):
    role: Union[str, None] = "editor"