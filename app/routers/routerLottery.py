from fastapi import APIRouter

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from BOT.util.generateDataReport import generate_data_for_report
from app.Schemas.SLottery import SLottery, SLotteryAddUpdate, SLotteryTicketsList
from app.config import settings
from app.dao.LotteryDAO import LotteryDAO
from app.Models.ModelsEnum import LotteryStatus, TicketStatus
from app.dao.TicketDAO import TicketDAO
from app.dao.TransactionExpenceDAO import TransactionExpenceDAO

router = APIRouter(
    prefix="/lottery",
    tags=["Лотереи"]
)
bot = Bot(token=settings.TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# Извлечение всех Лотерей без билетов
@router.get("")
async def get_all_lottery() -> list[SLottery]:
    return await LotteryDAO.get_model_all()


# Извлечение всех Лотерей по статусу без билетов
@router.get("/status")
async def get_lottery_by_status(status_lottery: LotteryStatus) -> list[SLottery]:
    return await LotteryDAO.get_model_all(status=status_lottery)


# Извлечение всех Лотерей по статусу с билетами
@router.get("/statusWithTickets")
async def get_lottery_by_status_with_tickets(status_lottery: LotteryStatus) -> list[SLotteryTicketsList]:
    return await LotteryDAO.get_lotterys_with_tickets_by_status(status=status_lottery)


# Получение количества оставшихся билетов лотереи
@router.get("/ostTicketLottery")
async def get_ost_tickets_lottery(id_lottery: int):
    lottery = await LotteryDAO.get_lottery_with_tickets_by_id(id_lottery)
    count_tickets = 0

    for i in lottery.tickets:
        if i.status == TicketStatus.OK:
            count_tickets = count_tickets + 1
    return lottery.number_tickets - count_tickets


# Розыгрыш лотереи
@router.get("/resultLottery/{id_lottery}")
async def result_lottery(id_lottery: int):
    if await get_ost_tickets_lottery(id_lottery) == 0:
        info_ticket = await TicketDAO.random_finish_ticket(id_lottery)
        await LotteryDAO.change_status(lottery_id=id_lottery,
                                       status=LotteryStatus.NONACTIVE)
        await bot.send_message(
            text=f'🏆 <em>Состоялся розыгрыш!</em> 🏆\n\n🎫 Лотерея: <b>{info_ticket[1]}</b>\n🎟 Выигрышный билет: <b>{info_ticket[0].number_ticket}</b>\n\n🏅 <b>Победитель</b> 🏅\n    🆔 {info_ticket[2]}\n    🙎‍♂️ @{info_ticket[3]}',
            chat_id='@cyber_loto')


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


# Изменение статуса Лотереи
@router.post("/changeStatus/{id_lottery}")
async def change_status_lottery(id_lottery: int, lottery_status: LotteryStatus):
    await LotteryDAO.change_status(lottery_id=id_lottery,
                                   status=lottery_status)


# Удаление Лотереи
@router.delete("/{id_lottery}")
async def delete_lottery(id_lottery: int):
    error = await LotteryDAO.delete_model(id_lottery)
    if error is not None:
        return error
