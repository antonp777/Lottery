from pydantic import BaseModel, ConfigDict

from app.Models.ModelsEnum import LotteryStatus
from app.Schemas.STicket import STicket


class SLottery(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    name: str
    number_tickets: int
    price_ticket: int
    status: LotteryStatus


class SLotteryTicketsList(SLottery):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    tickets: list[STicket]


class SLotteryAddUpdate(BaseModel):
    name: str
    number_tickets: int
    price_ticket: int
    status: LotteryStatus
