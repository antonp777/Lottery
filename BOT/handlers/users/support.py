from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from BOT.util.deleteMessage import *
from BOT.handlers.users.textForMessage import text_support

support = Router()


@support.message(F.text == '👨‍🔧 Поддержка')
async def support_(message: Message, bot: Bot):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Назад', callback_data='Главное меню'),
                InlineKeyboardButton(text='Перейти ➡️', url='https://t.me/cyberloto_supp')
            ]
        ]
    )

    await delete_message_user_bot(message, bot)
    await message.answer(text_support, reply_markup=keyboard)
