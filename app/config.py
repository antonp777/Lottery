import os
from typing import Optional

from pydantic import PostgresDsn, field_validator, ValidationInfo, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = Field(alias="DB_HOST")
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_BOT: str

    model_config = SettingsConfigDict(env_file=f'{os.path.dirname(os.path.abspath(__file__))}/../.env')

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_uri(cls, field_value, info: ValidationInfo) -> str:
        if isinstance(field_value, str):
            return field_value
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("DB_USER"),
            password=info.data.get("DB_PASSWORD"),
            host=info.data.get("DB_HOST"),
            port=info.data.get("DB_PORT"),
            path=info.data.get("DB_NAME") or "",
        ).unicode_string()


settings = Settings()