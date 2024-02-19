from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.Models.ModelsEnum import TransComingStatus
from app.database import Base, intpk, date


class TransactionComing(Base):
    __tablename__ = 'transactions_coming'
    id: Mapped[intpk]
    date: Mapped[date]
    sum: Mapped[int]
    comment: Mapped[str]
    status: Mapped[TransComingStatus]
    prichinaOtkaza: Mapped[str | None]
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_card: Mapped[int] = mapped_column(ForeignKey("cards.id"))
