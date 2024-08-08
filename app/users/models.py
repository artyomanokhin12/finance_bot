from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship

from app.database import Base
from app.incomes_bank.models import IncomesBank
from app.spendings_bank.models import SpendingsBank


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        unique=True, 
        autoincrement=False, 
        nullable=False
        )
    users_limit: Mapped[int | None] = mapped_column(Numeric)
    current_balance: Mapped[float | None] = mapped_column(Numeric)
    blocked: Mapped[bool | None]

    spendings_bank: Mapped[list['SpendingsBank']] = relationship()
    incomes_bank: Mapped[list['IncomesBank']] = relationship()


    def __repr__(self):
        return f'User={self.id}'
