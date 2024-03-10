from sqlalchemy import select, update
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

    @classmethod
    async def update_username_in_user(cls, chat_id: int, username: str):
        async with async_session() as session:
            query = update(User).where(User.chat_id == chat_id).values(username=username)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_mes_bot_in_user(cls, chat_id: int, last_message_id_bot: int):
        async with async_session() as session:
            query = update(User).where(User.chat_id == chat_id).values(last_message_id_bot=last_message_id_bot)
            await session.execute(query)
            await session.commit()

