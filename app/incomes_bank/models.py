import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.incomes.models import Incomes


class IncomesBank(Base):

    __tablename__ = "incomes_bank"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_fk: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    incomes_fk: Mapped[int] = mapped_column(ForeignKey("incomes.id"))
    amount: Mapped[float]
    operation_date: Mapped[datetime.datetime] = mapped_column(
        server_default=text("now()")
    )

    incomes: Mapped["Incomes"] = relationship()

    def __repr__(self):
        return f"Bank={self.user_fk}"
