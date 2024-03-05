from fastapi import APIRouter

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

