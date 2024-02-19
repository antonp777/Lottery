from pydantic import BaseModel, ConfigDict

from app.Models.ModelsEnum import LotteryStatus


class SLottery(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    number_tickets: int
    price_ticket: int
    status: LotteryStatus
class SLotteryAddUpdate(BaseModel):
    name: str
    number_tickets: int
    price_ticket: int
    status: LotteryStatus
