from sqlalchemy import select, func, desc

from app.Models.Lottery import Lottery
from app.Models.TransactionExpense import TransactionExpense
from app.dao.BaseDAO import BaseDAO
from app.dao.LotteryDAO import LotteryDAO
from app.database import async_session


class TransactionExpenceDAO(BaseDAO):
    model = TransactionExpense

    @classmethod
    async def add_trans_expence(cls, **data):
        async with async_session() as session:
            new_model = TransactionExpense(**data)
            session.add(new_model)
            await session.flush()
            await session.commit()
        return new_model.id

    @classmethod
    async def get_all_trans_expenses_join_lottery(cls, id_user: int):
        async with async_session() as session:
            result = await session.execute(
                select(TransactionExpense, Lottery.name)
                .where(TransactionExpense.id_user == id_user).join(Lottery).order_by(desc(TransactionExpense.id)))
            return result.all()

    @classmethod
    async def get_lottery_with_count_ticket_by_user(cls, id_user: int):
        async with async_session() as session:
            query = select(TransactionExpense.id_lottery,
                           func.sum(TransactionExpense.count_tickets)).where(
                TransactionExpense.id_user == id_user).group_by(TransactionExpense.id_lottery)
            result = await session.execute(query)
            res = result.all()
            data = []
            for row in res:
                lottery = await LotteryDAO.get_model_one(id=row[0])
                data.append({"name": lottery.name, "status": lottery.status, "count_tickets": row[1]})
            return data
