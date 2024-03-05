from aiogram.filters.callback_data import CallbackData


class LoterryInfo(CallbackData, prefix="lottery"):
    id: int
    priceTicket: int
    ostTicketForBuy: int


class ConfirmTransAdmin(CallbackData, prefix="confirmTransAdmin"):
    id_trans_coming: int
    id_trans_expense: int
    id_lottery: int
    id_user: int
    id_mes: int
    result: str
