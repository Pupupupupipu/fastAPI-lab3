from fastapi import APIRouter, Body
from typing import Union, Annotated
from models_old.User import User
from models_old.Admin import Admin
from models_old.UserDB import UserDB

router = APIRouter()

all_users = [
            User(id_user=1, name="Ivanov", age=22),
            UserDB(id_user=2, name="Petrov", age=25, password="asdfg"),
            Admin(id_user=3, name="Alex", age=23,id_admin=1, role="developer"),
            Admin(id_user=4, name="Ann", age=26, id_admin=2,)
            ]


def find_user(id:int) -> Union[User, None]:
    for user in all_users:
        if user.id_user == id:
            return user
    return None

@router.get('/users', response_model=Union[list[User], None])
def get_users():
    return all_users

@router.get('/users/{id}', response_model=Union[User, None])
def get_user(id: int):
    user = find_user(id)
    if user == None:
        return None
    return user

@router.post('/users', response_model=Union[User, None])
def create_user(new_user: Annotated[User, Body(embed=True, description="Новый пользователь")]):
    user = UserDB(name = new_user.name, age = new_user.age, id_user = new_user.id_user, password = new_user.name * 2 )
    all_users.append(user)
    return user

@router.post('/users/admin', response_model=Union[User, None])
def create_admin(new_user: Annotated[Admin, Body(embed=True, description="Новый администратор")]):
    user = Admin(name = new_user.name, age = new_user.age, id_user = new_user.id_user, password = new_user.name * 2, role = new_user.role)
    all_users.append(user)
    return user

@router.put('/users', response_model=Union[User, None])
def edit_user(needed_user: Annotated[User, Body(embed=True)]):
    user = find_user(needed_user.id_user)
    if user == None:
        return None
    user.name = needed_user.name
    user.age = needed_user.age
    return user

@router.delete('/users/{id}', response_model=Union[list[User], None])
def delete_user(id: int):
    user = find_user(id)
    if user == None:
        return None
    all_users.remove(user)
    return all_users

