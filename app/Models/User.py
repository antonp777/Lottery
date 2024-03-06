from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.Models.TransactionExpense import TransactionExpense
from app.database import Base, intpk


class User(Base):
    __tablename__ = 'users'
    id: Mapped[intpk]
    chat_id: Mapped[BigInteger] = mapped_column(BigInteger)
    username: Mapped[str | None]
    import app.Models.TransactionComing
    # transaction_coming = relationship("app.Models.TransactionComing.TransactionComing")
    transaction_coming: Mapped[list["app.Models.TransactionComing.TransactionComing"]] = relationship()
    transaction_expense: Mapped[list["TransactionExpense"]] = relationship()
    # tickets: Mapped[list["Ticket"]] = relationship(back_populates='Ticket.user')
