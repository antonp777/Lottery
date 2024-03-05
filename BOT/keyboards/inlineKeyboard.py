from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

inlineKeyboardGMenuCabinet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🕹 Главное меню', callback_data='Главное меню'),
            InlineKeyboardButton(text='💼 Личный кабинет', callback_data='Личный кабинет')
        ]
    ]
)
