from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.Models.ModelsEnum import TicketStatus
from app.Models.TransactionExpense import TransactionExpense
from app.database import Base, intpk


class Ticket(Base):
    __tablename__ = 'tickets'
    id: Mapped[intpk]
    number_ticket: Mapped[int | None]
    isFinish: Mapped[bool]
    status: Mapped[TicketStatus]
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_lottery: Mapped[int] = mapped_column(ForeignKey("lotterys.id"))
    id_trans_expense: Mapped[int] = mapped_column(ForeignKey("transactions_expense.id", ondelete="CASCADE"))

    trans_expense: Mapped[TransactionExpense] = relationship(back_populates="tickets")
    # lottery: Mapped[Lottery] = relationship(back_populates="tickets")
    # user: Mapped[User] = relationship(back_populates="tickets")
