from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.dao.base import BaseDAO
from app.spendings.models import Spendings
from app.database import async_session_maker


class SpendingsDAO(BaseDAO):

    model = Spendings
