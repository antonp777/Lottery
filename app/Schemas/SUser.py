from pydantic import BaseModel, ConfigDict

from app.Models.TransactionComing import TransactionComing
from app.Models.TransactionExpense import TransactionExpense


class SUser(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    chat_id: int


class SUserTrans(SUser):
    transaction_coming: list[TransactionComing]
    transaction_expense: list[TransactionExpense]


class SUserAddUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_id: int
