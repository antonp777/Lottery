from sqlalchemy.orm import Mapped

from app.database import Base, intpk


class UserAdmin(Base):
    __tablename__ = 'usersAdmin'
    id: Mapped[intpk]
    name: Mapped[str]
    password: Mapped[str]

