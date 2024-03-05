from datetime import timedelta, datetime, timezone

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from starlette import status

from app.config import settings
from app.dao.UserAdminDAO import UserAdminDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = (datetime.now(timezone.utc) + timedelta(minutes=720)).timestamp()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    existing_user = await UserAdminDAO.get_model_one(name=username)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверный логин")
    if not verify_password(password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверный пароль")
    return existing_user
