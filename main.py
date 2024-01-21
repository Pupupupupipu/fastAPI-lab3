from datetime import datetime
import uvicorn

from fastapi import FastAPI
from fastapi.responses import FileResponse
from db import init_db
from public.router_city import city_router
from public.router_country import country_router
from public.router_region import region_router

app = FastAPI()
#init_db()
#app.include_router(router)
app.include_router(country_router)
app.include_router(city_router)
app.include_router(region_router)


@app.on_event("startup")
def on_startup():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')
    init_db()

@app.on_event("shutdown")
def shutdown():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: End\n')

@app.get('/')
def main():
    return FileResponse("index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




