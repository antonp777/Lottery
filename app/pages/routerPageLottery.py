from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from app.Models.ModelsEnum import LotteryStatus
from app.Schemas.SLottery import SLotteryAddUpdate
from app.auth.dependencies import get_login_page
from app.routers.routerLottery import get_all_lottery, delete_lottery, create_lottery, get_lottery_by_id, \
    update_lottery, change_status_lottery

router = APIRouter(
    prefix="/ui",
    tags=["AdminPanel"]
)

templates = Jinja2Templates(directory="app/templates")


# Таблица со всеми лотереями
@router.get("/lottery")
async def page_lottery(request: Request,
                       lottery=Depends(get_all_lottery),
                       login_page=Depends(get_login_page)):
    return login_page if login_page else templates.TemplateResponse(name="lotterys/lotterys.html",
                                                                    context={
                                                                        "request": request,
                                                                        "lotterys": lottery})


# Добавление новой лотереи
@router.post("/lottery")
async def page_add_lottery(request: Request,
                           login_page=Depends(get_login_page),
                           name: str = Form(...),
                           number_tickets: int = Form(...),
                           price_ticket: int = Form()):
    if login_page:
        return login_page

    lottery = SLotteryAddUpdate(name=name,
                                number_tickets=number_tickets,
                                price_ticket=price_ticket,
                                status=LotteryStatus.NONACTIVE)
    await create_lottery(lottery)
    lotterys = await get_all_lottery()
    return templates.TemplateResponse(name="lotterys/lotterys.html",
                                      context={
                                          "request": request,
                                          "lotterys": lotterys})


# Открытие окна редактирования лотереи
@router.get("/lotteryEditModal/{id_lottery}")
async def page_edit_modal_lottery(id_lottery: int,
                                  request: Request):
    lottery = await get_lottery_by_id(id_lottery)
    return templates.TemplateResponse(name="lotterys/lotteryModalEdit.html",
                                      context={
                                          "request": request,
                                          "lottery": lottery})


# Изменение лотереи
@router.post("/lottery/edit")
async def page_edit_lottery(request: Request,
                            login_page=Depends(get_login_page),
                            id_lottery: int = Form(...),
                            name: str = Form(...),
                            number_tickets: int = Form(...),
                            price_ticket: int = Form(...),
                            status: str = Form()):
    if login_page:
        return login_page

    if status == "ACTIVE":
        status = LotteryStatus.ACTIVE
    else:
        status = LotteryStatus.NONACTIVE

    lottery = SLotteryAddUpdate(name=name,
                                number_tickets=number_tickets,
                                price_ticket=price_ticket,
                                status=status)
    await update_lottery(id_lottery, lottery)

    lotterys = await get_all_lottery()

    return templates.TemplateResponse(name="lotterys/lotterys.html",
                                      context={
                                          "request": request,
                                          "lotterys": lotterys})


# Открытие окна удаления лотереи
@router.get("/lotteryDeleteModal/{id_lottery}")
async def page_delete_modal_lottery(id_lottery: int,
                                    request: Request):

    return templates.TemplateResponse(name="lotterys/lotteryModalDelete.html",
                                      context={
                                          "request": request,
                                          'id_lottery': id_lottery})


# Удаление лотереи
@router.delete("/lottery")
async def page_delete_lottery(request: Request,
                              login_page=Depends(get_login_page)):
    if login_page:
        return login_page

    data = await request.body()
    id_lottery = int(data.decode().replace("id_lottery=", ""))
    await delete_lottery(id_lottery)
    lotterys = await get_all_lottery()
    return templates.TemplateResponse(name="lotterys/lotterys.html",
                                      context={
                                          "request": request,
                                          "lotterys": lotterys})


# Изменение статуса лотереи
@router.post("/lotteryStatus")
async def page_edit_status_lottery(request: Request,
                                   login_page=Depends(get_login_page)):
    if login_page:
        return login_page

    data = await request.body()
    id_lottery = int(data.decode().replace("id_lottery=", ""))

    lottery = await get_lottery_by_id(id_lottery)

    if lottery.status == LotteryStatus.ACTIVE:
        await change_status_lottery(id_lottery, LotteryStatus.NONACTIVE)
    else:
        await change_status_lottery(id_lottery, LotteryStatus.ACTIVE)

    lotterys = await get_all_lottery()

    return templates.TemplateResponse(name="lotterys/lotterys.html",
                                      context={
                                          "request": request,
                                          "lotterys": lotterys})
