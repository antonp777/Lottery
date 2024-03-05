from aiogram import Router, F, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from BOT.util.deleteMessage import *
# from filters.isAdmin import isAdmin
from BOT.handlers.users.textForMessage import text_general_menu
from app.routers.routerUser import add_user

generalMenuUsers = Router()
# generalMenuUsers.message.filter(~isAdmin())

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
    await add_user(message.from_user.id)

    await general_menu(bot=bot, message=message)


@generalMenuUsers.message(F.text == '🕹 Главное меню')
@generalMenuUsers.callback_query(F.data == 'Главное меню')
async def general_menu(message: Message | CallbackQuery,
                       bot: Bot,
                       state: FSMContext = None):
    if isinstance(message, Message):
        await message.answer(text_general_menu, reply_markup=keyboard)
        await delete_message_user_bot(message, bot)
    else:
        await state.clear()
        await message.message.answer(text_general_menu, reply_markup=keyboard)
        await delete_message_bot(message, bot)
