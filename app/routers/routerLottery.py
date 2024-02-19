from fastapi import APIRouter

from app.Validation.SLottery import SLottery, SLotteryAddUpdate
from app.dao.LotteryDAO import LotteryDAO
from app.Models.ModelsEnum import LotteryStatus

router = APIRouter(
    prefix="/lottery",
    tags=["Лотереи"]
)


# Извлечение всех Лотерей
@router.get("")
async def get_lottery_by_status(status_lottery: LotteryStatus) -> list[SLottery]:
    return await LotteryDAO.get_model_all(status=status_lottery)


# Извлечение Лотереи по id
@router.get("/{id_lottery}")
async def get_lottery_by_id(id_lottery: int) -> SLottery:
    return await LotteryDAO.get_model_by_id(id_lottery)


# Добавление Лотереи
@router.post("")
async def create_lottery(lottery_data: SLotteryAddUpdate):
    await LotteryDAO.add_model(name=lottery_data.name,
                               number_tickets=lottery_data.number_tickets,
                               price_ticket=lottery_data.price_ticket,
                               status=lottery_data.status)


# Изменение Лотереи
@router.post("/{id_lottery}")
async def update_lottery(id_lottery: int, lottery_data: SLotteryAddUpdate):
    await LotteryDAO.update_model(model_id=id_lottery,
                                  name=lottery_data.name,
                                  number_tickets=lottery_data.number_tickets,
                                  price_ticket=lottery_data.price_ticket,
                                  status=lottery_data.status)


# Удаление Лотереи
@router.delete("/{id_lottery}")
async def delete_lottery(id_lottery: int):
    await LotteryDAO.delete_model(id_lottery)
