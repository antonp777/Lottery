from pydantic import BaseModel, ConfigDict


class SUserAdmin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    password: str
