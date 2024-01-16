from config import settings
from sqlalchemy import text
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

ur_a = settings.POSTGRES_DATABASE_URLA

print(ur_a)

engine = create_async_engine(ur_a, connect_args={"check_same_thread": True}, echo=True)


async def f():
    async with engine.begin() as conn:
        answer = await conn.execute(text("select version()"))
        print(f"answer = {answer.all()}")


asyncio.run(f())