from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UsersSaving(Base):
    __tablename__ = "users_saving"

    id: Mapped[int] = mapped_column(primary_key=True)
    goal_name: Mapped[str]
    amount: Mapped[int]
    current_savings: Mapped[int | None]
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))

    def __repr__(self) -> str:
        return f"{self.goal_name} - Цель: {self.amount}, текущие сбережения: {self.current_savings}, осталось: {self.amount - self.current_savings}"
