from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database import Base

from bot.bank.models import Bank


class Users(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        unique=True, 
        autoincrement=False, 
        nullable=False
        )
    limit: Mapped[int | None] = mapped_column(Numeric)
    current_balance: Mapped[int | None] = mapped_column(Numeric)
    blocked: Mapped[bool | None]

    bank = relationship('Bank', back_populates='users')

    def __repr__(self):
        return f'User={self.id=}'
