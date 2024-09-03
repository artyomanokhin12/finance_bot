from sqlalchemy import delete, and_, update
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.saving.models import UsersSaving


class UsersSavingDAO(BaseDAO):

    model = UsersSaving


    @classmethod
    async def delete_saving(cls, user_id: int, goal_name: str) -> str:
        async with async_session_maker() as session:
            stmt = delete(UsersSaving).where(
                and_(
                    UsersSaving.user_id==user_id, 
                    UsersSaving.goal_name==goal_name
                )
            )
            await session.execute(stmt)
            await session.commit()
            return "Удаление записи прошло успешно"

    @classmethod
    async def update_goal(cls, user_id: int, goal_name: str, current_deposit: int) -> str:
        async with async_session_maker() as session:
            stmt = (
                update(UsersSaving)
                .where(
                    and_(
                        UsersSaving.user_id==user_id,
                        UsersSaving.goal_name==goal_name,
                    )
                )
                .values(current_savings=UsersSaving.current_savings + current_deposit)
            )
            await session.execute(stmt)
            await session.commit()
            return "Депозит внесен!"
