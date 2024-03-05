from aiogram import Router, F, Bot

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from BOT.util.deleteMessage import *
from BOT.keyboards.inlineKeys import inlineKeyGeneralMenu, inlineKeyCabinetMenu
from app.routers.routerTransactionComing import get_report_trans_coming
from app.routers.routerTransactionExpence import get_report_trans_expense
from app.routers.routerUser import get_user_by_chat_id

historyTrans = Router()


class PanaginationHistory(StatesGroup):
    filter_report = State()
    current_page = State()


category_trans = ['💵 Пополнения', '🎫 Покупки билетов']


def text_data(name_report, param1, param2, param3, param4, param5=None):
    if name_report == 'операции ' + category_trans[0]:
        result = f'<b>Операция: </b>{param1}\n<b>Дата:</b> {param2}\n<b>Сумма:</b> {param3}\n<b>Статус:</b> {param4}'
        if param5 is not None:
            result += f'\n<b>Причина:</b> {param5}'
    else:
        result = f'<b>Дата: </b>{param1}\n<b>Лотерея:</b> {param2}\n<b>Количество билетов:</b> {param3}\n<b>Сумма:</b> {param4}'
    return result


def page_pang(data_report, name_report, page):
    count_page = len(data_report.keys())

    text_mes: str = f'<em>{name_report}</em>\n\n'
    for value in data_report[page]:
        params = []
        for i in value.values():
            params.append(i)
            print(i)
        if len(params) > 4:
            text_mes = text_mes + text_data(name_report, params[0], params[1], params[2], params[3], params[4]) + '\n\n'
        else:
            text_mes = text_mes + text_data(name_report, params[0], params[1], params[2], params[3]) + '\n\n'

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


@historyTrans.message(F.text == '🔎 История операций', StateFilter(None))
async def list_filter_report(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(PanaginationHistory.filter_report)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=category_trans[0], callback_data='trans_coming_user')],
            [InlineKeyboardButton(text=category_trans[1], callback_data='trans_expense_user')],
            [inlineKeyCabinetMenu]
        ]
    )
    await delete_message_user_bot(message, bot)
    await message.answer('📍 Выберите категорию операции',
                         reply_markup=keyboard)


@historyTrans.callback_query(PanaginationHistory.filter_report)
async def show_fist_page(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(PanaginationHistory.current_page)

    id_user = await get_user_by_chat_id(callback.from_user.id)

    name_report = ''
    data_report = {}
    if callback.data == 'trans_coming_user':
        data_report = await get_report_trans_coming(id_user.id)
        name_report = 'операции ' + category_trans[0]
    elif callback.data == 'trans_expense_user':
        data_report = await get_report_trans_expense(id_user.id)
        name_report = 'операции ' + category_trans[1]

    # Ответ если нет данных для отчёта
    if data_report == {}:
        await delete_message_bot(callback, bot)
        await callback.message.answer('🤷 У Вас ещё нет истории в данной категории',
                                      reply_markup=InlineKeyboardMarkup(inline_keyboard=[[inlineKeyCabinetMenu]]))
    else:
        await state.update_data(data_report=data_report,
                                current_page=1,
                                name_report=name_report)

        param_answer = page_pang(data_report, name_report, 1)

        await delete_message_bot(callback, bot)

        await callback.message.answer(param_answer[0], reply_markup=param_answer[1])


@historyTrans.callback_query(PanaginationHistory.current_page)
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

    param_answer = page_pang(data_report, data_state['name_report'], page)

    await delete_message_bot(callback, bot)

    await callback.message.answer(param_answer[0], reply_markup=param_answer[1])
