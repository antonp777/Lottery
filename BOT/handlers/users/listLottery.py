from aiogram import Router, F, Bot
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from BOT.util.deleteMessage import delete_message_user_bot
from BOT.util.callbackData import *
from BOT.keyboards.inlineKeys import inlineKeyGeneralMenu
from BOT.handlers.users.textForMessage import text_list_lottery
from app.Models.ModelsEnum import LotteryStatus
from app.routers.routerLottery import get_lottery_by_status_with_tickets

listLottery = Router()


@listLottery.message(F.text == '📋 Список розыгрышей')
async def list_lottery(message: Message,
                       bot: Bot):
    # Выгрузка списка лотерей из БД со статусом активные
    list_lot = await get_lottery_by_status_with_tickets(LotteryStatus.ACTIVE)

    # Создание клавиатуры с названиями лотерей и количеством оставшихся и всего билетов лотереи
    keyboard = InlineKeyboardBuilder()

    for lot in list_lot:
        count_buy_ticket = len(lot.tickets)  # Количество билетов лотереи со всеми статусами
        ost_ticket_for_buy = lot.number_tickets - count_buy_ticket  # Количество оставшихся билетов лотереи
        keyboard.row(InlineKeyboardButton(text=f'{lot.name}\n({ost_ticket_for_buy}/{lot.number_tickets})',
                                          callback_data=LoterryInfo(id=lot.id,
                                                                    priceTicket=lot.price_ticket,
                                                                    ostTicketForBuy=ost_ticket_for_buy).pack()
                                          )
                     )

    # keyboard.adjust(2)
    keyboard.row(inlineKeyGeneralMenu)

    await delete_message_user_bot(message, bot)
    await message.answer(text_list_lottery, reply_markup=keyboard.as_markup())
