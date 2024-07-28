import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database import Base
from bot.incomes.models import Incomes
from bot.spendings.models import Spendings


class Bank(Base):

    __tablename__ = 'bank'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='RESTRICT'))
    spending_fk = mapped_column(ForeignKey('spendings.id'))
    incomes_fk: Mapped[int] = mapped_column(ForeignKey('incomes.id'))
    operation_date: Mapped[datetime.datetime] = mapped_column(server_default=text('now()'))

    users = relationship('Users', back_populates='bank')
    spendings = relationship('Spendings', back_populates='bank')
    incomes = relationship('Incomes' ,back_populates='bank')

    def __repr__(self):
        return f'Bank={self.user_fk=}'
