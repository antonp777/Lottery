from aiogram import Bot
from aiogram.types import Message, CallbackQuery


async def delete_message_user_bot(message: Message, bot: Bot):
    mes_user = message.message_id
    mes_bot = mes_user - 1
    chat_id = message.from_user.id

    await bot.delete_message(chat_id, mes_user)
    await bot.delete_message(chat_id, mes_bot)


async def delete_message_bot(callback: CallbackQuery, bot: Bot):
    chat_id = callback.from_user.id
    mes_id = callback.message.message_id

    await bot.delete_message(chat_id, mes_id)
