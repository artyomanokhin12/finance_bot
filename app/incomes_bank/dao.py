from sqlalchemy import insert
from app.dao.base import BaseDAO
from app.incomes_bank.models import IncomesBank
from app.database import async_session_maker

class IncomesBankDAO(BaseDAO):

    model = IncomesBank