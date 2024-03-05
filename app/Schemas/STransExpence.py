from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.Models.ModelsEnum import TransExpenseStatus
from app.Schemas.SLottery import SLottery


class STransactionExpense(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime
    sum: int
    count_tickets: int
    status: TransExpenseStatus
    id_user: int
    id_lottery: int


class STransactionExpenseAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sum: int
    count_tickets: int
    status: TransExpenseStatus
    id_user: int
    id_lottery: int
