from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Incomes(Base):
    __tablename__ = 'incomes'

    id: Mapped[int] = mapped_column(primary_key=True)
    incomes_name: Mapped[str | None]

    def __repr__(self):
        return self.incomes_name
