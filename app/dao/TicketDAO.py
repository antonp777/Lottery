import random

from sqlalchemy import select, update

from BOT.util.generateDataReport import generate_data_for_report
from app.Models.Lottery import Lottery
from app.Models.ModelsEnum import TicketStatus
from app.Models.Ticket import Ticket
from app.Models.User import User
from app.Schemas.STicket import STicketAdd, STicket
from app.dao.BaseDAO import BaseDAO
from app.database import async_session


class TicketDAO(BaseDAO):
    model = Ticket

    @classmethod
    async def add_all_tickets(cls, items_in: list[STicketAdd]):
        async with async_session() as session:
            list_tickets = [Ticket(**item.dict()) for item in items_in]
            session.add_all(list_tickets)
            await session.commit()

    @classmethod
    async def update_all_tickets(cls, id_trans: int, status_search: TicketStatus, **data):
        async with async_session() as session:
            query = update(Ticket).where(Ticket.id_trans_expense == id_trans).where(
                Ticket.status == status_search).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def random_finish_ticket(cls, id_lottery: int):
        async with async_session() as session:
            result = await session.execute(select(Ticket).where(Ticket.id_lottery == id_lottery))
            tickets = result.scalars().all()

            list_id_tickets = []

            for ticket in tickets:
                list_id_tickets.append(ticket.id)

            finish_id_ticket = random.choice(list_id_tickets)
            number_ticket_in_lottery = list_id_tickets.index(finish_id_ticket)+1

            finish_ticket = await session.get(Ticket, finish_id_ticket)
            finish_ticket.number_ticket = number_ticket_in_lottery
            finish_ticket.isFinish = True
            session.add(finish_ticket)
            await session.commit()

            result_ticket = await session.execute(select(Ticket, Lottery.name, User.chat_id, User.username)
                                                  .where(Ticket.id == finish_id_ticket)
                                                  .join(Lottery).join(User))

            info_ticket = result_ticket.one()

            return info_ticket

    @classmethod
    async def get_finish_ticket_by_user(cls, id_user: int):
        async with (async_session() as session):
            result = await session.execute(
                select(Lottery.name, Ticket.number_ticket)
                .filter(Ticket.id_user == id_user)
                .filter(Ticket.isFinish == True)
                .join(Lottery))

            res = result.all()

            data = []
            for i in res:
                data.append({'name': i[0], 'number_ticket': i[1]})

            return data
