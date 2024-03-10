from aiogram import Router, F

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from BOT.util.deleteMessage import *
from BOT.keyboards.inlineKeys import inlineKeyCabinetMenu
from app.Models.ModelsEnum import LotteryStatus
from app.routers.routerTicket import get_report_finish_ticket_by_user
from app.routers.routerTransactionExpence import get_report_lottery_for_user
from app.routers.routerUser import get_user_by_chat_id

myLottery = Router()


class Panagination(StatesGroup):
    filter_report = State()
    current_page = State()


category_lottery = ['⚡️ Активные розыгрыши', '💾 Завершённые розыгрыши', '🥇🏆🎗 Выигранные розыгрыши']


def text_data(name_report, param1, param2):
    if name_report == category_lottery[0] or name_report == category_lottery[1]:
        result = f'<b>Лотерея: </b>{param1}.\n<b>Куплено билетов:</b> {param2} шт.'
    else:
        result = f'<b>Лотерея: </b>{param1}.\n<b>Ваш выигрышный билет:</b> {param2}'
    return result


def page_pang(data_report, name_report, page):
    count_page = len(data_report.keys())

    text_mes: str = f'<em>{name_report}</em>\n\n'
    for value in data_report[page]:
        params = []
        for i in value.values():
            params.append(i)
        text_mes = text_mes + text_data(name_report, params[0], params[1]) + '\n\n'

    buttons = []
    if page == 1 and count_page > 1:
        buttons = [
            InlineKeyboardButton(text='▶️', callback_data='next_page'),
            InlineKeyboardButton(text='⏩', callback_data='end_page')
        ]

    elif page != 1 and page < count_page:
        buttons = [
            InlineKeyboardButton(text='⏪', callback_data='first_page'),
            InlineKeyboardButton(text='◀️', callback_data='previous_page'),
            InlineKeyboardButton(text='▶️', callback_data='next_page'),
            InlineKeyboardButton(text='⏩', callback_data='end_page')
        ]
    elif page == count_page and count_page > 1:
        buttons = [
            InlineKeyboardButton(text='⏪', callback_data='first_page'),
            InlineKeyboardButton(text='◀️', callback_data='previous_page'),
        ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons,
            [inlineKeyCabinetMenu]
        ]
    )

    return [text_mes, keyboard]


@myLottery.message(F.text == '👑 Мои розыгрыши', StateFilter(None))
async def list_filter_report(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(Panagination.filter_report)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=category_lottery[0], callback_data='active_user_lottery')],
            [InlineKeyboardButton(text=category_lottery[1], callback_data='not_active_user_lottery')],
            [InlineKeyboardButton(text=category_lottery[2], callback_data='winery_user_lottery')],
            [inlineKeyCabinetMenu]
        ]
    )
    await delete_message_user_bot(message, bot)
    await message.answer('📍 Выберите категорию розыгрыша',
                         reply_markup=keyboard)


@myLottery.callback_query(Panagination.filter_report)
async def show_fist_page(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(Panagination.current_page)

    id_user = await get_user_by_chat_id(callback.from_user.id)

    name_report = ''
    data_report = {}
    if callback.data == 'active_user_lottery':
        data_report = await get_report_lottery_for_user(id_user.id, LotteryStatus.ACTIVE)
        name_report = category_lottery[0]
    elif callback.data == 'not_active_user_lottery':
        data_report = await get_report_lottery_for_user(id_user.id, LotteryStatus.NONACTIVE)
        name_report = category_lottery[1]
    elif callback.data == 'winery_user_lottery':
        data_report = await get_report_finish_ticket_by_user(id_user.id)
        name_report = category_lottery[2]
    text_empty = '🤷 У Вас ещё нет истории в данной категории'

    # Ответ если нет данных для отчёта
    if data_report == {}:
        await delete_message_bot(callback, bot)
        await callback.message.answer(text_empty,
                                      reply_markup=InlineKeyboardMarkup(inline_keyboard=[[inlineKeyCabinetMenu]]))
    else:

        await state.update_data(data_report=data_report,
                                current_page=1,
                                name_report=name_report)

        param = page_pang(data_report, name_report, 1)

        await delete_message_bot(callback, bot)

        await callback.message.answer(param[0], reply_markup=param[1])


@myLottery.callback_query(Panagination.current_page)
async def next_page(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data_state = await state.get_data()
    data_report = data_state['data_report']
    current_page = data_state['current_page']

    page = 0
    if callback.data == 'next_page':
        page = current_page + 1
    elif callback.data == 'previous_page':
        page = current_page - 1
    elif callback.data == 'first_page':
        page = 1
    elif callback.data == 'end_page':
        page = len(data_report.keys())

    await state.update_data(current_page=page)

    param = page_pang(data_report, data_state['name_report'], page)

    await delete_message_bot(callback, bot)

    await callback.message.answer(param[0], reply_markup=param[1])
