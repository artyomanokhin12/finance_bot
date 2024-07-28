from sqlalchemy import insert, select, update

from bot.database import async_session_maker


class BaseDAO:

    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_all_by_filter(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def update_by_id(cls, id: int, limit: int):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id==id).values(limit=limit)
            await session.execute(stmt)
            await session.commit()
