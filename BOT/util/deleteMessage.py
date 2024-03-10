from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from app.routers.routerUser import get_user_by_chat_id


async def delete_message_user_bot(message: Message, bot: Bot):
    mes_user = message.message_id
    user = await get_user_by_chat_id(message.from_user.id)
    mes_bot = user.last_message_id_bot
    chat_id = message.from_user.id

    await bot.delete_message(chat_id, mes_user)
    await bot.delete_message(chat_id, mes_bot)

async def delete_message_user(message: Message, bot: Bot):
    mes_user = message.message_id
    chat_id = message.from_user.id

    await bot.delete_message(chat_id, mes_user)

async def delete_message_bot(callback: CallbackQuery, bot: Bot):
    chat_id = callback.from_user.id
    mes_id = callback.message.message_id
    await bot.delete_message(chat_id, mes_id)
