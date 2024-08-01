from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.dao.base import BaseDAO
from app.spendings.models import Spendings
from app.database import async_session_maker


class SpendingsDAO(BaseDAO):

    model = Spendings

    @classmethod
    async def find_all_test(cls):
        async with async_session_maker() as session:
            query = (
                select(Spendings)
                .options(joinedload(Spendings.bank))
            )
            result = await session.execute(query)
            return result.unique().scalars().all()
