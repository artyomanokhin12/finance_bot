from sqlalchemy import insert, update
from app.dao.base import BaseDAO
from app.incomes_bank.models import IncomesBank
from app.users.models import Users
from app.database import async_session_maker

class IncomesBankDAO(BaseDAO):

    model = IncomesBank

    @classmethod
    async def add(cls, **data):
        stmt_bank = insert(IncomesBank).values(**data)
        stmt_user = (
            update(Users)
            .where(Users.id == data['user_fk'])
            .values(current_balance = Users.current_balance + data['amount'])
        )

        async with async_session_maker() as session:
            await session.execute(stmt_bank)
            await session.execute(stmt_user)
            await session.commit()
            return 'Строка дохода успешно добавлена'
