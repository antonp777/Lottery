from sqlalchemy.orm import Mapped

from app.database import Base, intpk


class Card(Base):
    __tablename__ = 'cards'
    id: Mapped[intpk]
    number: Mapped[str]
