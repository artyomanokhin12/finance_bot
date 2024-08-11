import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.spendings.models import Spendings


class SpendingsBank(Base):

    __tablename__ = "spendings_bank"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_fk: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    spending_fk = mapped_column(ForeignKey("spendings.id"))
    amount: Mapped[float]
    operation_date: Mapped[datetime.datetime] = mapped_column(
        server_default=text("now()")
    )

    spendings: Mapped["Spendings"] = relationship()

    def __repr__(self):
        return f"Bank={self.user_fk}"
