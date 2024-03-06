from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from BOT.util.deleteMessage import *
from app.routers.routerUser import get_balance_user, get_user_by_chat_id, update_username_in_user

cabinetUser = Router()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='💳 Пополнить'),
        ],
        [
            KeyboardButton(text='👑 Мои розыгрыши'),
            KeyboardButton(text='🔎 История операций'),
        ],
        [
            KeyboardButton(text='🕹 Главное меню')  # --> user.generalMenuUsers
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите интересующий Вас пункт меню'
)


@cabinetUser.message(F.text == '💼 Личный кабинет')
@cabinetUser.callback_query(F.data == 'Личный кабинет')
async def menu_cabinet_user(message: Message | CallbackQuery,
                            bot: Bot,
                            state: FSMContext):
    await state.clear()

    text = f'💼 <u><b>Личный кабинет</b></u>\n\n🙎‍♂️ @{message.from_user.username}\n\n 🆔 {message.from_user.id}\n\n💰 Баланс: {await get_balance_user(chat_id=message.from_user.id)}'

    # Проверка username и при необходимости его обновления
    if message.from_user.username != await get_user_by_chat_id(message.from_user.id):
        await update_username_in_user(chat_id=message.from_user.id, username=message.from_user.username)

    if isinstance(message, Message):
        await delete_message_user_bot(message, bot)
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.message.answer(text, reply_markup=keyboard)
        await delete_message_bot(message, bot)
