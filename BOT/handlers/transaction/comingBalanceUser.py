from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from BOT.util.deleteMessage import *
from BOT.util.callbackData import *
from BOT.keyboards.inlineKeys import inlineKeyGeneralMenu, inlineKeyCabinetMenu, inlineKeyPeredumalCabinetMenu
from BOT.util.generateComment import generate_string
from app.Models.ModelsEnum import TransComingStatus
from app.Schemas.STransactionComing import STransactionComingAdd
from app.routers.routerCard import get_card_random
from app.routers.routerTransactionComing import add_trans_coming
from app.routers.routerUser import get_user_by_chat_id, update_username_in_user, update_last_mes_bot_in_user

comingBalanceUser = Router()


class ComingBalance(StatesGroup):
    sum_coming = State()
    sum_coming_error = State()
    confirm_pay = State()


# 1. Предложение ввести сумму для пополнения
@comingBalanceUser.message(F.text == '💳 Пополнить', StateFilter(None))
@comingBalanceUser.callback_query(F.data == 'return_sum_coming', ComingBalance.sum_coming_error)
async def query_sum_coming(message: Message | CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(ComingBalance.sum_coming)
    text = '✍️ Введите сумму для пополнения'
    if isinstance(message, Message):
        await delete_message_user_bot(message, bot)
        msg = await message.answer(text,
                             reply_markup=InlineKeyboardMarkup(
                                 inline_keyboard=[[inlineKeyPeredumalCabinetMenu]]))
        await update_last_mes_bot_in_user(chat_id=message.from_user.id, mes_id=msg.message_id)
    else:
        await delete_message_bot(message, bot)
        msg = await message.message.answer(text,
                                     reply_markup=InlineKeyboardMarkup(
                                         inline_keyboard=[[inlineKeyPeredumalCabinetMenu]]))
        await update_last_mes_bot_in_user(chat_id=message.from_user.id, mes_id=msg.message_id)

# 2. Подтверждение перевода
@comingBalanceUser.message(F.text.regexp(r"^(\d+)$"), ComingBalance.sum_coming)
async def sum_coming(message: Message, bot: Bot, state: FSMContext):
    # Генерация рандомной карты из БД
    card = await get_card_random()
    # Генерация комментария
    comment = generate_string(8)

    # id User в БД
    user = await get_user_by_chat_id(chat_id=message.from_user.id)

    # Проверка username и при необходимости его обновления
    if message.from_user.username != user.username:
        await update_username_in_user(chat_id=message.from_user.id, username=message.from_user.username)

    await state.set_state(ComingBalance.confirm_pay)
    await state.update_data(card=card[1],
                            card_number=card[0],
                            comment=comment,
                            sum_coming=message.text,
                            id_user=user.id)

    keyboard = InlineKeyboardBuilder().add(inlineKeyPeredumalCabinetMenu,
                                           InlineKeyboardButton(
                                               text="✅ Оплатил ✅",
                                               callback_data='confirm_pay'
                                           )).adjust(2)

    await delete_message_user_bot(message, bot)
    await message.answer(
        f'💵 Сумма пополнения: <b>{message.text}</b> руб.\n'
        f'💳 Реквизиты: <b>{card[0]}</b>\n'
        f'❗️ Переведите <b>точную сумму</b> и <b>обязательно</b> укажите комментарий к переводу: <b>{comment}</b>️️ ❗️',
        reply_markup=keyboard.as_markup()
    )


# 2.1. ОШИБКА ПРИ ВВОДЕ СУММЫ ПОПОЛНЕНИЯ (ВВЕДЕНО НЕ ЧИСЛО)
@comingBalanceUser.message(~F.text.regexp(r"^(\d+)$"), ComingBalance.sum_coming)
async def error_sum_coming(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(ComingBalance.sum_coming_error)

    text = 'Ошибка ввода: Вы ввели не число!\nKоличество билетов должно быть только число!'
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [inlineKeyPeredumalCabinetMenu,
             InlineKeyboardButton(text='✍️ Повторить ввод', callback_data='return_sum_coming')
             ]
        ]
    )
    await delete_message_user_bot(message, bot)
    await message.answer(text, reply_markup=keyboard)



# 3. Формирование обработки перевода
@comingBalanceUser.callback_query(F.data == 'confirm_pay', ComingBalance.confirm_pay)
async def post_trans_to_admin(callback: CallbackQuery,
                              bot: Bot,
                              state: FSMContext):
    data_state = await state.get_data()

    # Ответ для User
    await delete_message_bot(callback, bot)
    msg = await callback.message.answer(
        '🔁 Ваша операция обрабатывается!\n❗ Пожалуйста не предпринимайте никаких действий и дождитесь подтверждения.')

    # Добавление ПРИХОДНОЙ транзакции со статусом ОЖИДАНИЕ
    trans_coming = STransactionComingAdd(
        sum=data_state['sum_coming'],
        comment=data_state['comment'],
        status=TransComingStatus.WAIT,
        id_trans_expence_info=None,
        message_id=msg.message_id,
        id_user=data_state['id_user'],
        id_card=int(data_state['card'])
    )
    await add_trans_coming(trans_coming)
    await state.clear()
