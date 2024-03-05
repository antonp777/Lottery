from fastapi import APIRouter

from app.Models.ModelsEnum import TransComingStatus, TransExpenseStatus
from app.Schemas.SUser import SUserAddUpdate
from app.dao.UserDAO import UserDAO

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"]
)


@router.post("")
async def add_user(chat_id: int):
    user_find = await UserDAO.get_model_one(chat_id=chat_id)
    if not user_find:
        await UserDAO.add_model(chat_id=chat_id)

@router.get("/chat_id")
async def get_user_by_chat_id(chat_id: int):
    return await UserDAO.get_model_one(chat_id=chat_id)

# Баланс User по chat_id
@router.get("/balanceUser/{chat_id}")
async def get_balance_user(chat_id: int):
    user = await UserDAO.get_user_with_trans(chat_id=chat_id)

    coming_sum = 0
    for i in user.transaction_coming:
        if i.status == TransComingStatus.OK:
            coming_sum = coming_sum + i.sum

    expense_sum = 0
    for i in user.transaction_expense:
        if i.status == TransExpenseStatus.OK:
            expense_sum = expense_sum + i.sum

    return coming_sum - expense_sum

