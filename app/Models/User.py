from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.Models import TransactionComing, TransactionExpense
from app.database import Base, intpk


class User(Base):
    __tablename__ = 'users'
    id: Mapped[intpk]
    chat_id: Mapped[BigInteger] = mapped_column(BigInteger)
    transaction_coming: Mapped[list["TransactionComing"]] = relationship()
    transaction_expense: Mapped[list["TransactionExpense"]] = relationship()
    #tickets: Mapped[list["Ticket"]] = relationship(back_populates='Ticket.user')
