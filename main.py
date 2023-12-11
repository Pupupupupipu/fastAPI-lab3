from fastapi import FastAPI
from methods import router

users = []
admins = []

app = FastAPI()
app.include_router(router)





