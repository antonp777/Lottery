from sqlalchemy.orm import Mapped, relationship

from app.Models import Ticket
from app.Models.ModelsEnum import LotteryStatus
from app.database import Base, intpk


class Lottery(Base):
    __tablename__ = 'lotterys'
    id: Mapped[intpk]
    name: Mapped[str]
    number_tickets: Mapped[int]
    price_ticket: Mapped[int]
    status: Mapped[LotteryStatus]
    tickets: Mapped[list["Ticket"]] = relationship()
