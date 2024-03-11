from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates


from app.Models.UserAdmin import UserAdmin
from app.Schemas.SUserAdmin import SUserAdmin
from app.auth.dependencies import get_current_user_admin
from app.config import settings
from app.routers.routerAuth import login

router = APIRouter(
    prefix="/ui",
    tags=["AdminPanel"]
)

templates = Jinja2Templates(directory=settings.get_app_root()+"/app/templates")


@router.get("/")
async def admin_panel_index(request: Request, user: UserAdmin = Depends(get_current_user_admin)):
    if not user:
        return templates.TemplateResponse(name="login.html", context={"request": request})
    return templates.TemplateResponse(name="index.html",
                                      context={"request": request})


@router.post("/login")
async def admin_panel_login(request: Request, name: str = Form(...), password: str = Form(...)):
    user = SUserAdmin(name=name, password=password)
    response = templates.TemplateResponse(name="index.html", context={"request": request})
    access_token = await login(response, user)
    if access_token:
        return response
