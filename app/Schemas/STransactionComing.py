from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.Models.ModelsEnum import TransComingStatus
from app.Schemas.SCard import SCard
from app.Schemas.SUser import SUser


class STransactionComing(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime
    sum: int
    comment: str
    status: TransComingStatus
    prichinaOtkaza: Optional[str]
    id_user: int
    id_card: int


class STransactionComingAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    sum: int
    comment: str
    status: TransComingStatus
    message_id: int
    id_trans_expence_info: Optional[int]
    id_user: int
    id_card: int


class STransactionComingUserCard(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    date: datetime
    sum: int
    comment: str
    status: TransComingStatus
    prichinaOtkaza: Optional[str]
    user: SUser
    card: SCard


class STransactionComingUpdateStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: TransComingStatus


class STransactionComingUpdateStatusPrichina(STransactionComingUpdateStatus):
    prichinaOtkaza: str
