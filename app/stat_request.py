import datetime

from sqlalchemy import select, func, and_

from app.database import async_session_maker
from app.spendings_bank.models import SpendingsBank
from app.spendings.models import Spendings
from app.incomes_bank.models import IncomesBank
from app.users.models import Users


async def get_stats(user_id: int, date_from: datetime.date, date_to: datetime.date):
    
    async with async_session_maker() as session:
        spend_true = (
            select(SpendingsBank.user_fk, func.sum(SpendingsBank.amount).label('sum_amount_true'))
            .select_from(SpendingsBank)
            .where(
                and_(
                    SpendingsBank.spending_fk.in_(
                        select(Spendings.id)
                        .select_from(Spendings)
                        .filter_by(optional_spending=True)
                    ),
                    and_(
                        SpendingsBank.operation_date >= date_from,
                        SpendingsBank.operation_date < date_to,
                    ),
                ),
            )
            .group_by(SpendingsBank.user_fk)
            .cte('spend_true')
        )

        spend_false = (
            select(SpendingsBank.user_fk, func.sum(SpendingsBank.amount).label('sum_amount_false'))
            .select_from(SpendingsBank)
            .where(
                and_(
                    SpendingsBank.spending_fk.in_(
                        select(Spendings.id)
                        .select_from(Spendings)
                        .filter_by(optional_spending=False)
                    ),
                    and_(
                        SpendingsBank.operation_date >= date_from,
                        SpendingsBank.operation_date < date_to,
                    ),
                ),
            )
            .group_by(SpendingsBank.user_fk)
            .cte('spend_false')
        )
    
        incomes_all = (
            select(IncomesBank.user_fk, func.sum(IncomesBank.amount).label('sum_incomes'))
            .select_from(IncomesBank)
            .where(
                and_(
                    IncomesBank.user_fk == user_id,
                    and_(
                        IncomesBank.operation_date >= date_from,
                        IncomesBank.operation_date < date_to,
                    )
                )
            )
            .group_by(IncomesBank.user_fk)
            .cte('incomes_all')
        )

        spend_all_month = (
            select(SpendingsBank.user_fk, func.sum(SpendingsBank.amount).label('sum_all_time'))
            .where(
                and_(
                    SpendingsBank.operation_date >= datetime.date.today().replace(day=1),
                    SpendingsBank.operation_date <= datetime.date.today() + datetime.timedelta(days=1)
                )
            )
            .group_by(SpendingsBank.user_fk)
            .cte('spend_all_month')
        )

        query = (
            select(
                spend_true.c.sum_amount_true.label('Потрачено на основные категории'),
                spend_false.c.sum_amount_false.label('Потрачено на не основные категории'),
                (spend_true.c.sum_amount_true + spend_false.c.sum_amount_false).label('Потрачено всего'),
                incomes_all.c.sum_incomes.label('Получено всего'),
                Users.current_balance.label('Текущий баланс'),
                (Users.users_limit - spend_all_month.c.sum_all_time).label('Остаток от лимита')
            )
            .select_from(Users)
            .join(spend_true, Users.id == spend_true.c.user_fk, isouter=True)
            .join(spend_false, Users.id == spend_false.c.user_fk, isouter=True)
            .join(incomes_all, Users.id == incomes_all.c.user_fk, isouter=True)
            .join(spend_all_month, Users.id == spend_all_month.c.user_fk, isouter=True)
            .where(Users.id == user_id)
        )
        result = await session.execute(query)
        result = result.mappings().one_or_none()

        result_str = ''
        for key, value in result.items():
            if key in ('Текущий баланс', 'Отстаток от лимита'):
                value = float(value)
            if value is None:
                value = 0
            result_str = result_str + f'{key}: {value}' + '\n'

        return result_str
