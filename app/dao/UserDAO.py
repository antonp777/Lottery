from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.Models.User import User
from app.Schemas.SUser import SUserTrans

from app.dao.BaseDAO import BaseDAO
from app.database import async_session


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_user_with_trans(cls, chat_id: int) -> SUserTrans:
        async with async_session() as session:
            query = select(User).filter_by(chat_id=chat_id).options(joinedload(cls.model.transaction_coming)).options(
                joinedload(cls.model.transaction_expense))
            result = await session.execute(query)
            exist_model = result.unique().scalar_one()
            return exist_model

