from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.Models.ModelsEnum import LotteryStatus, TicketStatus
from app.Models.Ticket import Ticket
from app.Models.TransactionExpense import TransactionExpense
from app.dao.BaseDAO import BaseDAO
from app.Models.Lottery import Lottery
from app.database import async_session


class LotteryDAO(BaseDAO):
    model = Lottery

    @classmethod
    async def change_status(cls, lottery_id: int, status: LotteryStatus):
        async with async_session() as session:
            lottery = await session.get(Lottery, lottery_id)
            lottery.status = status
            await session.commit()

    @classmethod
    async def get_lotterys_with_tickets_by_status(cls, status: LotteryStatus):
        async with async_session() as session:
            query = select(Lottery).where(Lottery.status == status).options(selectinload(Lottery.tickets))
            result = await session.execute(query)
            lotterys = result.unique().scalars().all()
            return lotterys

    # Получение количества оставшихся билетов лотереи
    @classmethod
    async def get_lottery_with_tickets_by_id(cls, id_lottery: int):
        async with async_session() as session:
            query = select(Lottery).where(Lottery.id == id_lottery).options(
                selectinload(Lottery.tickets))
            result = await session.execute(query)
            lottery = result.unique().scalar_one()
            return lottery

    @classmethod
    async def get_report_lottery_user(cls, id_user: int):
        async with async_session() as session:
            await session.execute(select(Lottery).where(Lottery))

            result = await session.execute(
                select(Lottery.name, Lottery.status, func.sum(TransactionExpense.count_tickets))
                .where(TransactionExpense.id_user == id_user)
                .group_by(TransactionExpense.id_lottery)
                .join(Lottery)
                )
        return result.all()
