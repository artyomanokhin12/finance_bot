from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database import Base

class Incomes(Base):

    __tablename__ = 'incomes'

    id: Mapped[int] = mapped_column(primary_key=True)
    incomes_name: Mapped[str]

    bank = relationship('Bank', back_populates='incomes')
