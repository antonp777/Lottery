from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.Models.ModelsEnum import TransComingStatus
from app.database import Base, intpk, date

from app.Models import User
from app.Models import Card


class TransactionComing(Base):
    __tablename__ = 'transactions_coming'
    id: Mapped[intpk]
    date: Mapped[date]
    sum: Mapped[int]
    comment: Mapped[str]
    status: Mapped[TransComingStatus]
    prichinaOtkaza: Mapped[str | None]
    message_id: Mapped[int | None]
    id_trans_expence_info: Mapped[int | None]
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_card: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    user = relationship("app.Models.User.User", back_populates="transaction_coming")
    card = relationship("app.Models.Card.Card", back_populates="transaction_coming")
