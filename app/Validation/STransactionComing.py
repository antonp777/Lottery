from typing import Optional
from datetime import date

from pydantic import BaseModel, ConfigDict

from app.Models.ModelsEnum import TransComingStatus


class STransactionComing(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date
    sum: int
    comment: str
    status: TransComingStatus
    prichinaOtkaza: Optional[str]
    id_user: int
    id_card: int


class STransactionComingUpdateStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: TransComingStatus
