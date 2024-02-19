from fastapi import HTTPException
from sqlalchemy import select, insert, delete, update
from starlette import status

from app.database import async_session


class BaseDAO:
    model = None

    # Извлечение всех моделей
    @classmethod
    async def get_model_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            exist_model = result.scalars().all()
            if not exist_model:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return exist_model

    # Извлечение модели по любому полю(полям)
    @classmethod
    async def get_model_one(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    # Извлечение модели по id
    @classmethod
    async def get_model_by_id(cls, model_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            exist_model = result.scalar_one_or_none()
            if not exist_model:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return exist_model

    # Добавление модели
    @classmethod
    async def add_model(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    # Изменение модели
    @classmethod
    async def update_model(cls, model_id: int, **data):
        async with async_session() as session:
            await cls.get_model_by_id(model_id)
            query = update(cls.model).where(cls.model.id == model_id).values(data)
            await session.execute(query)
            await session.commit()

    # Удаление модели
    @classmethod
    async def delete_model(cls, model_id):
        async with async_session() as session:
            await cls.get_model_by_id(model_id)
            query = delete(cls.model).filter_by(id=model_id)
            await session.execute(query)
            await session.commit()
