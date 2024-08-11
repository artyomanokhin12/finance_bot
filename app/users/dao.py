from sqlalchemy import delete

from app.dao.base import BaseDAO
from app.users.models import Users

from app.database import async_session_maker

class UsersDAO(BaseDAO):

    model = Users

    @classmethod
    async def delete(cls, user_id: int):
        async with async_session_maker() as session:
            stmt = delete(Users).where(Users.id == user_id)
            await session.execute(stmt)
            await session.commit()
            return 'Удаление прошло успешено'