import asyncio
import json

from sqlalchemy import insert

from app.database import async_session_maker
from app.incomes.models import Incomes
from app.spendings.models import Spendings

async def add_data():

    def open_json(model: str):
        with open(f"./app/data/{model}.json", "r") as file:
            return json.load(file)
        
    incomes = open_json("incomes")
    spendings = open_json("spendings")

    async with async_session_maker() as session:
        incomes = insert(Incomes).values(incomes)
        spendings = insert(Spendings).values(spendings)

        await session.execute(incomes)
        await session.execute(spendings)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_data())
