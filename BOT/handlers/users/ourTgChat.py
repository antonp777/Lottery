from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from BOT.util.deleteMessage import *
from BOT.handlers.users.textForMessage import text_tg_chanel

ourTgChat = Router()


@ourTgChat.message(F.text == '📲 Наш Telegram-канал')
async def our_tg_chat(message: Message, bot: Bot):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Назад', callback_data='Главное меню'),
                InlineKeyboardButton(text='Перейти ➡️', url='https://t.me/cyber_loto')
            ]
        ]
    )

    await delete_message_user_bot(message, bot)
    await message.answer(text_tg_chanel, reply_markup=keyboard)
