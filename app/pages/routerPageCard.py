from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates

from app.Schemas.SCard import SCardAddUpdate
from app.auth.dependencies import get_login_page
from app.routers.routerCard import get_card_all, delete_card, add_card, get_card_one_by_id, update_card

router = APIRouter(
    prefix="/ui",
    tags=["AdminPanel"]
)

templates = Jinja2Templates(directory="../app/templates")


# Таблица со всеми картами
@router.get("/cards")
async def page_card(request: Request,
                    cards=Depends(get_card_all),
                    login_page=Depends(get_login_page)):
    return login_page if login_page else templates.TemplateResponse(name="cards/cards.html",
                                                                    context={
                                                                        "request": request,
                                                                        'cards': cards})


# Добавление новой карты
@router.post("/card")
async def page_add_card(request: Request,
                        login_page=Depends(get_login_page),
                        number: str = Form()):
    if login_page:
        return login_page

    card = SCardAddUpdate(number=number)
    await add_card(card)
    cards = await get_card_all()
    return templates.TemplateResponse(name="cards/cards.html",
                                      context={"request": request,
                                               "cards": cards})


# Открытие окна редактирования карты
@router.get("/cardEditModal/{id_card}")
async def page_edit_modal_card(id_card: int,
                               request: Request):
    card = await get_card_one_by_id(id_card)
    return templates.TemplateResponse(name="cards/cardModalEdit.html",
                                      context={
                                          "request": request,
                                          "card": card})


# Изменение карты
@router.post("/card/edit")
async def page_edit_lottery(request: Request,
                            login_page=Depends(get_login_page),
                            id_card: int = Form(...),
                            number: str = Form(...)):
    if login_page:
        return login_page

    card = SCardAddUpdate(number=number)
    await update_card(id_card, card)

    cards = await get_card_all()
    return templates.TemplateResponse(name="cards/cards.html",
                                      context={
                                          "request": request,
                                          "cards": cards})


# Открытие окна удаления карты
@router.get("/cardDeleteModal/{id_card}")
async def page_card(id_card: int,
                    request: Request):
    return templates.TemplateResponse(name="cards/cardModalDelete.html",
                                      context={
                                          "request": request,
                                          'id_card': id_card})


# Удаление карты
@router.delete("/card")
async def page_card(request: Request,
                    login_page=Depends(get_login_page)):
    if login_page:
        return login_page

    data = await request.body()
    id_card = int(data.decode().replace("id_card=", ""))
    await delete_card(id_card)
    cards = await get_card_all()
    return templates.TemplateResponse(name="cards/cards.html",
                                      context={
                                          "request": request,
                                          'cards': cards})
