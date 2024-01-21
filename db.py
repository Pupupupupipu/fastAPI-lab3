from sqlalchemy.ext.asyncio import create_async_engine

from config import settings
from sqlalchemy import text, create_engine
import asyncio

from models.country import Base

ur_a = settings.POSTGRES_DATABASE_URLS

print(ur_a)

engine = create_engine(ur_a, echo=True)

def init_db():
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def f():
    with engine.begin() as conn:
        answer = conn.execute(text("select * from country;"))
        print(f"answer = {answer.all()}")


f()
#asyncio.get_event_loop().run_until_complete(f())