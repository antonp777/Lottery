from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext



from BOT.keyboards.inlineKeyboard import inlineKeyboardGMenuCabinet
from BOT.util.deleteMessage import *
from BOT.util.callbackData import *
from BOT.keyboards.inlineKeys import inlineKeyGeneralMenu, inlineKeyPeredumalGeneralMenu

from BOT.util.generateComment import generate_string
from app.Models.ModelsEnum import TransExpenseStatus, TicketStatus, TransComingStatus
from app.Schemas.STicket import STicket, STicketAdd
from app.Schemas.STransExpence import STransactionExpenseAdd
from app.Schemas.STransactionComing import STransactionComing, STransactionComingAdd
from app.routers.routerCard import get_card_random
from app.routers.routerLottery import result_lottery
from app.routers.routerTicket import add_tickets
from app.routers.routerTransactionComing import add_trans_coming_with_id
from app.routers.routerTransactionExpence import add_trans_expence, add_trans_expence_with_id
from app.routers.routerUser import get_balance_user, get_user_by_chat_id, update_username_in_user, \
    update_last_mes_bot_in_user

buyTickets = Router()


class BuyTickets(StatesGroup):
    count_tickets = State()
    count_tickets_error = State()
    confirm_buy = State()
    confirm_pay = State()


# 1. Предложение ввести количество билетов для покупки
@buyTickets.callback_query(LoterryInfo.filter(F.id > 0), StateFilter(None))
@buyTickets.callback_query(F.data == 'return_buy_tickets', BuyTickets.count_tickets_error)
async def buy_tickets(callback: CallbackQuery,
                      bot: Bot,
                      state: FSMContext,
                      callback_data: LoterryInfo = None):
    keyboard = InlineKeyboardBuilder().row(inlineKeyGeneralMenu)

    ost_tickets_for_buy: int

    if callback_data:
        await state.update_data(id_lottery=callback_data.id,
                                price_ticket=callback_data.priceTicket,
                                ost_tickets_for_buy=callback_data.ostTicketForBuy)

        ost_tickets_for_buy = callback_data.ostTicketForBuy
    else:
        data_state = await state.get_data()
        ost_tickets_for_buy = data_state['ost_tickets_for_buy']

    await delete_message_bot(callback, bot)
    msg = await callback.message.answer(
        f'ℹ️ Доступно для покупки <b>{ost_tickets_for_buy} бил.</b>\n✍️ Введите количество билетов, которое хотите приобрести, но не более 500 шт.',
        reply_markup=keyboard.as_markup()
    )
    await update_last_mes_bot_in_user(chat_id=callback.from_user.id, mes_id=msg.message_id)

    await state.set_state(BuyTickets.count_tickets)



# 2.1. Подтверждение покупки билетов
@buyTickets.message(F.text.regexp(r"^(\d+)$"), BuyTickets.count_tickets)
async def count_tickets_for_buy(message: Message,
                                bot: Bot,
                                state: FSMContext):
    data_state = await state.get_data()

    # ПРОВЕРКА НА КОЛИЧЕСТВО БИЛЕТОВ
    if int(message.text) <= data_state['ost_tickets_for_buy'] and int(message.text) < 500:

        await state.update_data(count_tickets=int(message.text))
        keyboard = InlineKeyboardBuilder().add(inlineKeyPeredumalGeneralMenu,
                                               InlineKeyboardButton(text='✅ Подтвердить ✅',
                                                                    callback_data='buyTickets_ok')
                                               )

        await delete_message_user_bot(message, bot)
        await state.set_state(BuyTickets.confirm_buy)

        data_state = await state.get_data()

        await message.answer(
            f"Вы хотите купить <b>{message.text}</b> бил.\nОбщая стоимость составляет <b>{data_state['price_ticket'] * int(message.text)}</b> руб.",
            reply_markup=keyboard.as_markup()
        )
    else:
        text = 'Вы ввели не допустимое количество билетов'
        await count_tickets_for_buy_error(message, bot, state, text)


# 2.2. ОШИБКА ПРИ ВВОДЕ КОЛИЧЕСТВА БИЛЕТОВ (ВВЕДЕНО НЕ ЧИСЛО)
@buyTickets.message(~F.text.regexp(r"^(\d+)$"), BuyTickets.count_tickets)
async def count_tickets_for_buy_error(message: Message,
                                      bot: Bot,
                                      state: FSMContext,
                                      text: str = None):
    await state.set_state(BuyTickets.count_tickets_error)

    if text is None:
        text = '‼️ Ошибка ввода: Вы ввели не число!\nKоличество билетов должно быть только число!'
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [inlineKeyPeredumalGeneralMenu,
             InlineKeyboardButton(text='✍️ Повторить ввод', callback_data='return_buy_tickets')
             ]
        ]
    )
    await delete_message_user_bot(message, bot)

    await message.answer(text, reply_markup=keyboard)



# 3. Подтверждение оплаты от User/Покупка билетов с баланса User
@buyTickets.callback_query(F.data == 'buyTickets_ok', BuyTickets.confirm_buy)
async def confirm_buy_at_user(callback: CallbackQuery,
                              bot: Bot,
                              state: FSMContext):
    data_state = await state.get_data()

    coast_tickets: int = data_state['count_tickets'] * data_state['price_ticket']
    balance_user = await get_balance_user(callback.from_user.id)

    user = await get_user_by_chat_id(callback.from_user.id)

    # Проверка username и при необходимости его обновления
    if callback.from_user.username != user.username:
        await update_username_in_user(chat_id=callback.from_user.id, username=callback.from_user.username)

    # Если БАЛАНС User МЕНЬШЕ стоимости билетов
    if balance_user < coast_tickets:
        # Генерация рандомной карты из БД
        card = await get_card_random()
        # Генерация комментария
        comment = generate_string(8)
        # Сумма для оплаты
        sum_for_pay = coast_tickets - balance_user

        await state.set_state(BuyTickets.confirm_pay)
        await state.update_data(card=card[1], card_number=card[0], comment=comment, sum_for_pay=sum_for_pay,
                                id_user=user.id)

        keyboard = InlineKeyboardBuilder().add(inlineKeyPeredumalGeneralMenu,
                                               InlineKeyboardButton(
                                                   text="✅ Оплатил ✅",
                                                   callback_data='confirm_pay'
                                               )).adjust(2)

        await callback.message.answer(
            f'💵 Сумма пополнения: <b>{sum_for_pay}</b> руб.\n'
            f'💳 Реквизиты: <b>{card[0]}</b>\n'
            f'❗️ Переведите <b>точную сумму</b> и <b>обязательно</b> укажите комментарий к переводу: <b>{comment}</b> ❗️\n\n'
            f'<em>Время на оплату 30 минут, во избежания аннулирования вашей заявки, оплатите в отведенное время, либо создайте новую</em>',
            reply_markup=keyboard.as_markup()
        )
        await delete_message_bot(callback, bot)

    # Если БАЛАНС User БОЛЬШЕ стоимости билетов
    else:
        # Создание Транзакции РАСХОДА
        trans_expense = STransactionExpenseAdd(
            sum=coast_tickets,
            count_tickets=int(data_state['count_tickets']),
            status=TransExpenseStatus.OK,
            id_user=user.id,
            id_lottery=int(data_state['id_lottery'])
        )

        # Добавление Транзакции Расхода в БД
        id_trans = await add_trans_expence_with_id(trans_expense)

        # Создание Билетов в БД
        tickets = []
        i = 1
        while i <= data_state['count_tickets']:
            ticket = STicketAdd(
                id_user=user.id,
                isFinish=False,
                id_lottery=data_state['id_lottery'],
                id_trans_expense=id_trans,
                status=TicketStatus.OK
            )
            tickets.append(ticket)
            i += 1

        # Добавление Билетов в БД
        await add_tickets(tickets)

        await delete_message_bot(callback, bot)

        await callback.message.answer(f"Вы успешно приобрели {data_state['count_tickets']} шт. билетов",
                                      reply_markup=inlineKeyboardGMenuCabinet)

        # Розыгрыш лотереи
        await result_lottery(data_state['id_lottery'])
        await state.clear()


# 4. Отправка данных на подтверждение Admin
@buyTickets.callback_query(F.data == 'confirm_pay', BuyTickets.confirm_pay)
async def post_trans_to_admin(callback: CallbackQuery,
                              bot: Bot,
                              state: FSMContext):
    data_state = await state.get_data()

    # Ответ для User
    msg = await callback.message.answer(
        '🔁 Ваша операция обрабатывается!\n❗ Пожалуйста не предпринимайте никаких действий и дождитесь подтверждения.')
    id_mes = msg.message_id
    await delete_message_bot(callback, bot)

    # Добавление РАСХОДНОЙ транзакции со статусом ОЖИДАНИЕ

    trans_expense = STransactionExpenseAdd(
        id_user=data_state['id_user'],
        sum=data_state['count_tickets'] * data_state['price_ticket'],
        count_tickets=data_state['count_tickets'],
        id_lottery=data_state['id_lottery'],
        status=TransExpenseStatus.WAIT
    )

    id_trans_expense = await add_trans_expence_with_id(trans_expense)
    ######################################

    # Добавление ПРИХОДНОЙ транзакции со статусом ОЖИДАНИЕ
    trans_coming = STransactionComingAdd(
        sum=data_state['sum_for_pay'],
        comment=data_state['comment'],
        status=TransComingStatus.WAIT,
        message_id=id_mes,
        id_trans_expence_info=id_trans_expense,
        id_user=data_state['id_user'],
        id_card=int(data_state['card'])
    )
    await add_trans_coming_with_id(trans_coming)
    ##############################

    await state.clear()
