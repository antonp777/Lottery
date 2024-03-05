from aiogram import Bot, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from BOT.handlers.users.textForMessage import text_rules_game

from BOT.util.deleteMessage import *

rulesGame = Router()


@rulesGame.message(F.text == '🤝 Честная игра')
async def rules_game(message: Message, bot: Bot):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Ознакомился', callback_data='Главное меню')
            ]
        ]
    )

    await message.answer(text_rules_game,
                         reply_markup=keyboard)
    await delete_message_user_bot(message, bot)
