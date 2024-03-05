from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.Models.ModelsEnum import TransExpenseStatus

from app.database import Base, intpk, date


class TransactionExpense(Base):
    __tablename__ = 'transactions_expense'
    id: Mapped[intpk]
    date: Mapped[date]
    sum: Mapped[int]
    count_tickets: Mapped[int]
    status: Mapped[TransExpenseStatus]  # Ok/wait
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_lottery: Mapped[int] = mapped_column(ForeignKey("lotterys.id"))
    tickets: Mapped[list["app.Models.Ticket.Ticket"]] = relationship(back_populates="trans_expense", cascade="all, delete-orphan",
                                                   passive_deletes=True)
    # tickets: Mapped[list["Ticket"]] = relationship()
    # lottery: Mapped[Lottery] = relationship()
