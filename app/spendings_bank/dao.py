from app.dao.base import BaseDAO
from app.spendings_bank.models import SpendingsBank


class SpendingsBankDAO(BaseDAO):

    model = SpendingsBank
