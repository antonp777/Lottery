import random

from sqlalchemy import select

from app.dao.BaseDAO import BaseDAO
from app.Models.Card import Card
from app.database import async_session


class CardDAO(BaseDAO):
    model = Card


    # Получение рандомного номера карты
    @classmethod
    async def get_random_card(cls):
        async with async_session() as session:
            query = select(Card)
            result = await session.execute(query)
            card = result.unique().scalars().all()

            number_card = {}
            for i in card:
                number_card[i.number] = i.id

            return random.choice(list(number_card.items()))
