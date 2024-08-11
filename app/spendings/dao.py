from app.dao.base import BaseDAO
from app.spendings.models import Spendings


class SpendingsDAO(BaseDAO):

    model = Spendings
