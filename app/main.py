import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.routerUser import router as routerUser
from app.routers.routerCard import router as routerCard
from app.routers.routerLottery import router as routerLottery
from app.routers.routerTicket import router as routerTicket
from app.routers.routerTransactionComing import router as routerTransComing
from app.routers.routerTransactionExpence import router as routerTransExpence
from app.routers.routerAuth import router as routerAuth
from app.auth.auth_docs import router as token

from app.pages.router import router as router_pages
from app.pages.routerPageLottery import router as router_ui_lottery
from app.pages.routerPageCard import router as router_ui_card
from app.pages.routerPageTransComing import router as router_ui_trans_coming

app = FastAPI(openapi_prefix="/api", title="API Lottery", version="1.0.0")

origins = [
    "http://localhost:8000",
    "http://0.0.0.0:8000",
    "http://localhost:7777"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "Set-Coolie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow"],
)

app.include_router(token)
app.include_router(routerAuth)
app.include_router(routerUser)
app.include_router(routerLottery)
app.include_router(routerCard)
app.include_router(routerTicket)
app.include_router(routerTransExpence)
app.include_router(routerTransComing)
app.include_router(router_pages)
app.include_router(router_ui_lottery)
app.include_router(router_ui_card)
app.include_router(router_ui_trans_coming)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000)
