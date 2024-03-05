from fastapi import APIRouter, HTTPException, Response
from starlette import status

from app.Schemas.SUserAdmin import SUserAdmin
from app.auth.utils import get_password_hash, verify_password, authenticate_user, create_access_token
from app.dao.UserAdminDAO import UserAdminDAO

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register(user: SUserAdmin):
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
