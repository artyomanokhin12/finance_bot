from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Spendings(Base):
    __tablename__ = 'spendings'

    id: Mapped[int] = mapped_column(primary_key=True)
    spendings_name: Mapped[str]
    optional_spending: Mapped[bool]

    def __repr__(self):
        return self.spendings_name
