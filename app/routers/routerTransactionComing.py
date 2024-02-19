from fastapi import APIRouter

from app.Validation.STransactionComing import STransactionComing, STransactionComingUpdateStatus
from app.dao.TransactionComingDAO import TransactionComingDAO

router = APIRouter(
    prefix="/transComing",
    tags=["Транзакции Пополнения"]
)


@router.get("")
async def get_transComing() -> list[STransactionComing]:
    return await TransactionComingDAO.get_model_all()


# Изменение Статуса Транзакции
@router.post("/{id_card}")
async def update_status_transComing(id_trans: int, trans_data: STransactionComingUpdateStatus):
    await TransactionComingDAO.update_model(model_id=id_trans, status=trans_data.status)
