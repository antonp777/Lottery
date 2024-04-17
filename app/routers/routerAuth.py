from typing import Annotated

from fastapi import APIRouter, HTTPException, Response, Depends


from starlette import status


from app.Schemas.SUserAdmin import SUserAdmin, SUserAdminIdName
from app.auth.auth_docs import SuperAdmin, get_current_active_user
from app.auth.utils import get_password_hash, verify_password, authenticate_user, create_access_token
from app.dao.UserAdminDAO import UserAdminDAO

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
@router.get("/get_all_user")
async def get_all_user(current_user: Annotated[SuperAdmin, Depends(get_current_active_user)]) -> list[SUserAdminIdName]:
    return await UserAdminDAO.get_model_all()


@router.post("/register")
async def register(current_user: Annotated[SuperAdmin, Depends(get_current_active_user)], user: SUserAdmin):
    existing_user = await UserAdminDAO.get_model_one(name=user.name)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой пользователь существует")
    hashed_password = get_password_hash(user.password)
    await UserAdminDAO.add_model(name=user.name, password=hashed_password)


@router.post("/login")
async def login(response: Response, user: SUserAdmin):
    existing_user = await authenticate_user(username=user.name, password=user.password)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверно указаны имя или пароль")
    access_token = create_access_token({"sub": str(existing_user.id)})
    response.set_cookie("access_token_ui", access_token, httponly=True)
    return access_token

@router.post("/change_password")
async def change_password(current_user: Annotated[SuperAdmin, Depends(get_current_active_user)], id_user: int, new_password: str):
    new_password_hash = get_password_hash(new_password)
    await UserAdminDAO.update_model(model_id=id_user, password=new_password_hash)


@router.delete("/delete_user")
async def delete_user(current_user: Annotated[SuperAdmin, Depends(get_current_active_user)], id_user: int):
    await UserAdminDAO.delete_model(model_id=id_user)
