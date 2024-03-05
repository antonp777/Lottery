from pydantic import BaseModel, ConfigDict


# Вывод из БД
class SCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str


# Добавление в БД
class SCardAddUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    number: str
