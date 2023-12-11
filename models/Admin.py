from typing import Union
from models.User import User

class Admin(User):
    role: Union[str, None] = "editor"