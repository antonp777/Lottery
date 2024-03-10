from aiogram import Router, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from BOT.util.deleteMessage import *
from BOT.handlers.users.textForMessage import text_general_menu

from app.routers.routerUser import add_user, update_last_mes_bot_in_user

generalMenuUsers = Router()

text_keyboard_menu = ['📋 Список розыгрышей', '💼 Личный кабинет', '📲 Наш Telegram-канал', '👨‍🔧 Поддержка', '🤝 Честная игра', '🕹 Главное меню']
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📋 Список розыгрышей'),  # --> user.listLottery
            KeyboardButton(text='💼 Личный кабинет')  # --> user.cabinetUser
        ],
        [
            KeyboardButton(text='📲 Наш Telegram-канал'),  # --> user.ourTgChat
            KeyboardButton(text='👨‍🔧 Поддержка'),  # --> user.support
        ],
        [
            KeyboardButton(text='🤝 Честная игра')  # --> user.rulesGame
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите интересующий Вас пункт меню'
)


@generalMenuUsers.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    await add_user(message.from_user.id, message.from_user.username)

    await general_menu(bot=bot, message=message)


@generalMenuUsers.message(F.text == '🕹 Главное меню')
@generalMenuUsers.callback_query(F.data == 'Главное меню')
async def general_menu(message: Message | CallbackQuery,
                       bot: Bot,
                       state: FSMContext = None):
    if isinstance(message, Message):
        if message.text == '/start':
            await delete_message_user(message, bot)
        else:
            await delete_message_user_bot(message, bot)

        msg = await message.answer(text_general_menu, reply_markup=keyboard)
        await update_last_mes_bot_in_user(chat_id=message.from_user.id, mes_id=msg.message_id)
    else:
        await state.clear()
        msg = await message.message.answer(text_general_menu, reply_markup=keyboard)
        await update_last_mes_bot_in_user(chat_id=message.from_user.id, mes_id=msg.message_id)
        await delete_message_bot(message, bot)
