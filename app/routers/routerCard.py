from fastapi import APIRouter

from app.Schemas.SCard import SCard, SCardAddUpdate
from app.dao.CardDAO import CardDAO

router = APIRouter(
    prefix="/card",
    tags=["Карты"]
)


# Извлечение всех Карт
@router.get("")
async def get_card_all() -> list[SCard]:
    return await CardDAO.get_model_all()

# Получение рандомного номера карты
@router.get("/randomCard")
async def get_card_random():
    return await CardDAO.get_random_card()

# Извлечение Карты по id
@router.get("/{id_card}")
async def get_card_one_by_id(id_card: int) -> SCard:
    return await CardDAO.get_model_by_id(id_card)


# Добавление Карты
@router.post("")
async def add_card(card_data: SCardAddUpdate):
    await CardDAO.add_model(number=card_data.number)


# Изменение Карты
@router.post("/{id_card}")
async def update_card(id_card: int, card_data: SCardAddUpdate):
    await CardDAO.update_model(model_id=id_card, number=card_data.number)


# Удаление Карты
@router.delete("/{id_card}")
async def delete_card(id_card: int):
    await CardDAO.delete_model(id_card)
