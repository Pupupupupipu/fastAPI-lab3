import datetime
import uvicorn

from fastapi import FastAPI
from methods import router
from public.routers import init_db, country_router


app = FastAPI()
#app.include_router(router)
app.include_router(country_router)

@app.on_event("startup")
def on_startup():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')
    init_db()

@app.on_event("shutdown")
def shutdown():
    open("log.txt", mode="a").write(f'{datetime.utcnow()}: End\n')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




