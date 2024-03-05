from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from starlette import status


from app.Models.ModelsEnum import TransComingStatus
from app.Schemas.STransactionComing import STransactionComingAdd, STransactionComing
from app.dao.BaseDAO import BaseDAO
from app.Models.TransactionComing import TransactionComing
from app.database import async_session


class TransactionComingDAO(BaseDAO):
    model = TransactionComing

    @classmethod
    async def get_trans_coming_user_card(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by).options(joinedload(cls.model.user)).options(
                joinedload(cls.model.card)).order_by(
                desc(cls.model.id))
            result = await session.execute(query)
            exist_model = result.unique().scalars().all()
            return exist_model

    @classmethod
    async def add_trans_coming(cls, **data):
        async with async_session() as session:
            new_model = TransactionComing(**data)
            session.add(new_model)
            await session.flush()
            await session.commit()
        return new_model.id


