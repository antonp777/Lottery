from fastapi import APIRouter

from BOT.util.generateDataReport import generate_data_for_report
from app.Models.ModelsEnum import TicketStatus
from app.Schemas.STicket import STicketAdd
from app.dao.TicketDAO import TicketDAO

router = APIRouter(
    prefix="/ticket",
    tags=["Билеты"]
)

@router.post("/tickets")
async def add_tickets(tickets: list[STicketAdd]):
    return await TicketDAO.add_all_tickets(tickets)

@router.post("/updateStatus")
async def update_tickets_status(id_trans_exp: int, status_search: TicketStatus, new_status: TicketStatus):
    await TicketDAO.update_all_tickets(id_trans=id_trans_exp, status_search=status_search, status=new_status)

# Выгрузка данных из БД для отчёта по выигранным лотереям
@router.get("/reportFinishTicketByUser")
async def get_report_finish_ticket_by_user(id_user: int):
    list_ticket = await TicketDAO.get_finish_ticket_by_user(id_user)

    return generate_data_for_report(list_ticket, 2)
