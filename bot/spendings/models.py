from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database import Base


class Spendings(Base):

    __tablename__ = 'spendings'

    id: Mapped[int] = mapped_column(primary_key=True)
    spendings_name: Mapped[str]
    optional_spending: Mapped[bool]

    bank = relationship('Bank', back_populates='spendings')
