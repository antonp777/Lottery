from sqlalchemy.orm import Mapped, relationship

from app.database import Base, intpk

class Card(Base):
    __tablename__ = 'cards'
    id: Mapped[intpk]
    number: Mapped[str]
    transaction_coming = relationship("app.Models.TransactionComing.TransactionComing", back_populates="card")
