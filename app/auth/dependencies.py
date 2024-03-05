from datetime import datetime, timezone

from fastapi import Request, HTTPException, Depends
from jose import JWTError, jwt
from starlette import status

from fastapi.templating import Jinja2Templates

from app.config import settings
from app.dao.UserAdminDAO import UserAdminDAO

templates = Jinja2Templates(directory="../app/templates")

async def get_current_user_admin(request: Request):
    token = request.cookies.get("access_token_ui")
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        return None
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        return None
    user_id = int(payload.get("sub"))
    if not user_id:
        return None
    user = await UserAdminDAO.get_model_by_id(user_id)
    return user


async def get_login_page(request: Request, user=Depends(get_current_user_admin)):
    if not user:
        response = templates.TemplateResponse(name="login.html", context={"request": request})
        response.headers['HX-Reswap'] = 'outerHTML'
        response.headers['HX-Retarget'] = '#index'
        response.headers['HX-Reselect'] = '#auth'
        return response
