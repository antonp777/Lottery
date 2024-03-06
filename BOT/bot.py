import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from app.config import settings

from BOT.handlers.ListHandlersUsers import *
from BOT.handlers.ListHandlersTrans import *


async def main():

    bot = Bot(token=settings.TOKEN_BOT, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(
        generalMenuUsers,
        listLottery,
        cabinetUser,
        ourTgChat,
        support,
        rulesGame,
        buyTickets,
        comingBalanceUser,
        myLottery,
        historyTrans
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
