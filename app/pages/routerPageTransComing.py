import datetime
import json

from fastapi import APIRouter, Request, Depends, Form, Body
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict

from app.Models.ModelsEnum import TransComingStatus
from app.Schemas.STransactionComing import STransactionComingUpdateStatus, STransactionComingUpdateStatusPrichina
from app.auth.dependencies import get_login_page
from app.config import settings
from app.routers.routerTransactionComing import get_trans_coming_user_card, update_status_trans_coming, \
    update_status_prichina_trans_coming, get_trans_coming_user_card_status

router = APIRouter(
    prefix="/ui",
    tags=["AdminPanel"]
)

templates = Jinja2Templates(directory=settings.get_app_root()+"/app/templates")


def min_message_ago(date: datetime):
    return int((datetime.datetime.now() - date).total_seconds() // 60)


templates.env.globals.update(min_message_ago=min_message_ago)


# Таблица со всеми транзакциями
@router.get("/transComing")
async def page_trans_coming(request: Request,
                            trans=Depends(get_trans_coming_user_card),
                            login_page=Depends(get_login_page)):
    return login_page if login_page else templates.TemplateResponse(name="transComing/transComing.html",
                                                                    context={
                                                                        "request": request,
                                                                        "trans": trans})
@router.get("/updateTableTransComing")
async def update_table_lottery(request: Request,
                               trans=Depends(get_trans_coming_user_card),
                               login_page=Depends(get_login_page)):
    return login_page if login_page else templates.TemplateResponse(name="transComing/tableTransComing.html",
                                                                    context={
                                                                        "request": request,
                                                                        "trans": trans})

# Подтверждение транзакции
@router.post("/transComing/success")
async def page_trans_coming_success(request: Request,
                                    login_page=Depends(get_login_page)):
    if login_page:
        return login_page

    data = await request.body()
    trans_id = int(data.decode().replace("id=", ""))

    status = STransactionComingUpdateStatus(status=TransComingStatus.OK)
    await update_status_trans_coming(trans_id, status)

    trans = await get_trans_coming_user_card()
    return templates.TemplateResponse(name="transComing/transComing.html",
                                      context={"request": request, "trans": trans})


# Модальное окно для отклонения транзакции
@router.get("/transComingModal/{trans_id}")
async def page_trans_coming_modal(trans_id: int,
                                  request: Request):
    return templates.TemplateResponse(name="transComing/transComingModal.html",
                                      context={
                                          "request": request,
                                          "trans_id": trans_id})


# Отклонение транзакции
@router.post("/transComing/not-success")
async def page_trans_coming_not_success(request: Request,
                                        login_page=Depends(get_login_page),
                                        prichina_otkaza: str = Form(...),
                                        trans_id: int = Form(...)):
    if login_page:
        return login_page

    status_prichina = STransactionComingUpdateStatusPrichina(status=TransComingStatus.NOTOK,
                                                             prichinaOtkaza=prichina_otkaza)
    await update_status_prichina_trans_coming(trans_id, status_prichina)
    trans = await get_trans_coming_user_card()
    return templates.TemplateResponse(name="transComing/transComing.html",
                                      context={
                                          "request": request,
                                          "trans": trans})


@router.get("/transComingMessage")
async def page_trans_coming_modal(request: Request,
                                  login_page=Depends(get_login_page)):
    if login_page:
        return login_page

    trans = await get_trans_coming_user_card_status(TransComingStatus.WAIT)

    if trans is not None:
        return templates.TemplateResponse(name="transComing/transComingMessage.html",
                                          context={
                                              "request": request,
                                                "trans": trans,
                                                "time_now": datetime.datetime.now()})
    # else:
    #     return templates.TemplateResponse(name="transComing.html",
    #                                       context={"request": request})
