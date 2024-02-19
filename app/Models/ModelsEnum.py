from enum import Enum


class LotteryStatus(Enum):
    ACTIVE = 'ACTIVE'
    NONACTIVE = 'NONACTIVE'


class TicketStatus(Enum):
    OK = 'OK'
    WAIT = 'WAIT'


class TransExpenseStatus(Enum):
    OK = 'OK'
    WAIT = 'WAIT'


class TransComingStatus(Enum):
    OK = 'OK'
    NOTOK = 'NOTOK'
    WAIT = 'WAIT'