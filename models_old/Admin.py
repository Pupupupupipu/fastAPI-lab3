from typing import Union
from models_old.UserDB import UserDB

class Admin(UserDB):
    id_admin: Union[int, None] = None
    role: Union[str, None] = "editor"