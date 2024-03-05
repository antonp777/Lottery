from pydantic import BaseModel, ConfigDict

from app.Models.ModelsEnum import TicketStatus


class STicket(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    isFinish: bool
    status: TicketStatus
    id_user: int
    id_lottery: int
    id_trans_expense: int

class STicketAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    isFinish: bool
    status: TicketStatus
    id_user: int
    id_lottery: int
    id_trans_expense: int