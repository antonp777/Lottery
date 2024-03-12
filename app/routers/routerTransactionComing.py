from fastapi import APIRouter

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot
from BOT.keyboards.inlineKeyboard import inlineKeyboardGMenuCabinet
from BOT.util.generateDataReport import generate_data_for_report
from app.Models.ModelsEnum import TransExpenseStatus, TicketStatus
from app.Schemas.STicket import STicketAdd

from app.Schemas.STransactionComing import *
from app.config import settings
from app.dao.TransactionComingDAO import TransactionComingDAO
from app.dao.TransactionExpenceDAO import TransactionExpenceDAO
from app.dao.UserDAO import UserDAO
from app.routers.routerLottery import result_lottery, get_ost_tickets_lottery, get_lottery_by_id
from app.routers.routerTicket import update_tickets_status, add_tickets
from app.routers.routerTransactionExpence import update_status_trans_expence, delete_trans_expence, \
    update_status_sum_count_tickets_trans_expence

router = APIRouter(
    prefix="/transComing",
    tags=["Транзакции Пополнения"]
)
bot = Bot(token=settings.TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


# Все транзакции
@router.get("")
async def get_trans_coming() -> list[STransactionComing]:
    return await TransactionComingDAO.get_model_all()


# Все транзакции с данными User и Card
@router.get("/full")
async def get_trans_coming_user_card() -> list[STransactionComingUserCard]:
    return await TransactionComingDAO.get_trans_coming_user_card()


@router.get("/full_status")
async def get_trans_coming_user_card_status(status: TransComingStatus) -> list[STransactionComingUserCard]:
    return await TransactionComingDAO.get_trans_coming_user_card(status=status)


# Добавление транзакции
@router.post("")
async def add_trans_coming(trans_data: STransactionComingAdd):
    return await TransactionComingDAO.add_model(sum=trans_data.sum,
                                                comment=trans_data.comment,
                                                status=trans_data.status,
                                                message_id=trans_data.message_id,
                                                id_user=trans_data.id_user,
                                                id_card=trans_data.id_card)


# Добавление транзакции с ответом id
@router.post("/add")
async def add_trans_coming_with_id(data: STransactionComingAdd):
    return await TransactionComingDAO.add_trans_coming(sum=data.sum,
                                                       comment=data.comment,
                                                       status=data.status,
                                                       message_id=data.message_id,
                                                       id_trans_expence_info=data.id_trans_expence_info,
                                                       id_user=data.id_user,
                                                       id_card=data.id_card)


# Изменение Статуса Транзакции
@router.post("status/{id_trans}")
async def update_status_trans_coming(id_trans: int, trans_data: STransactionComingUpdateStatus):
    trans = await TransactionComingDAO.get_model_one(id=id_trans)
    user = await UserDAO.get_model_one(id=trans.id_user)

    text_message = ''

    if trans.id_trans_expence_info is not None:
        trans_exp = await TransactionExpenceDAO.get_model_one(id=trans.id_trans_expence_info)
        ost_tickets_lottery = await get_ost_tickets_lottery(trans_exp.id_lottery)
        # Если остаток билетов в лотерее больше или равен количеству покупаемых билетам
        if ost_tickets_lottery >= trans_exp.count_tickets:

            await update_status_trans_expence(id_trans=trans.id_trans_expence_info, status=TransExpenseStatus.OK)

            # Создание Билетов в БД
            tickets = []
            i = 1
            while i <= trans_exp.count_tickets:
                ticket = STicketAdd(
                    id_user=user.id,
                    isFinish=False,
                    id_lottery=trans_exp.id_lottery,
                    id_trans_expense=trans.id_trans_expence_info,
                    status=TicketStatus.OK
                )
                tickets.append(ticket)
                i += 1
            await add_tickets(tickets)

            # Розыгрыш лотереи
            await result_lottery(trans_exp.id_lottery)

            text_message = f'✅ Ваша покупка успешно проведена. Вы приобрели {trans_exp.count_tickets} бил.'

        # Если остаток билетов в лотерее меньше количества покупаемых билетов, но не равен нулю
        elif (ost_tickets_lottery < trans_exp.count_tickets) and (ost_tickets_lottery != 0):

            lottery = await get_lottery_by_id(id_lottery=trans_exp.id_lottery)
            new_sum = lottery.price_ticket*ost_tickets_lottery
            await update_status_sum_count_tickets_trans_expence(id_trans=trans.id_trans_expence_info, status=TransExpenseStatus.OK, sum=new_sum, count_tickets=ost_tickets_lottery)

            # Создание Билетов в БД
            tickets = []
            i = 1
            while i <= ost_tickets_lottery:
                ticket = STicketAdd(
                    id_user=user.id,
                    isFinish=False,
                    id_lottery=trans_exp.id_lottery,
                    id_trans_expense=trans.id_trans_expence_info,
                    status=TicketStatus.OK
                )
                tickets.append(ticket)
                i += 1
            await add_tickets(tickets)

            # Розыгрыш лотереи
            await result_lottery(trans_exp.id_lottery)

            text_message = f'✅ Ваша покупка успешно проведена.\nК сожалению Вам удалось приобрести только {ost_tickets_lottery} бил., так как их быстро разбирают!\nОстаток денежных средств зачислены на Ваш баланс.'

        elif ost_tickets_lottery == 0:
            await delete_trans_expence(id_trans=trans.id_trans_expence_info)
            text_message = f'✅ Ваша операция успешно проведена.\nК сожалению Вам не удалось приобрести билеты, так как их быстро разбирают!\nДенежные средства зачислены на Ваш баланс.'

    elif trans.id_trans_expence_info is None:


        text_message = f'✅ Ваш баланс пополнен на сумму {trans.sum} руб.'


    await bot.delete_message(chat_id=user.chat_id, message_id=trans.message_id)
    await bot.send_message(chat_id=user.chat_id, text=text_message, reply_markup=inlineKeyboardGMenuCabinet)

    await TransactionComingDAO.update_model(model_id=id_trans, status=trans_data.status)


# Изменение Статуса Транзакции и добавление причины
@router.post("status_prichina/{id_trans}")
async def update_status_prichina_trans_coming(id_trans: int, trans_data: STransactionComingUpdateStatusPrichina):
    trans = await TransactionComingDAO.get_model_one(id=id_trans)
    user = await UserDAO.get_model_one(id=trans.id_user)

    text_message = f'⛔️ Ваш платёж отклонён по причине: {trans_data.prichinaOtkaza}\nПри возникновении дополнительных вопросов обращайтесь в поддержку!'
    await bot.delete_message(chat_id=user.chat_id, message_id=trans.message_id)
    await bot.send_message(chat_id=user.chat_id, text=text_message, reply_markup=inlineKeyboardGMenuCabinet)

    await TransactionComingDAO.update_model(model_id=id_trans, status=trans_data.status,
                                            prichinaOtkaza=trans_data.prichinaOtkaza)

    if trans.id_trans_expence_info is not None:
        await delete_trans_expence(id_trans=trans.id_trans_expence_info)


@router.get("/report")
async def get_report_trans_coming(id_user: int):
    list_result = await TransactionComingDAO.get_model_all(id_user=id_user)

    list_trans_coming = []
    for i in list_result:

        item = {'id': i.id, 'date': i.date.strftime('%d.%m.%Y %H:%M'), 'sum': i.sum}
        if i.status == TransComingStatus.OK:
            item['status'] = 'проведена'
        elif i.status == TransComingStatus.NOTOK:
            item['status'] = 'отклонена'
            item['prichinaOtkaza'] = i.prichinaOtkaza
        elif i.status == TransComingStatus.WAIT:
            item['status'] = 'ожидание проведения'

        list_trans_coming.append(item)
    return generate_data_for_report(list_trans_coming, 2)
