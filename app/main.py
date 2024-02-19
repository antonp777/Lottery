import uvicorn
from fastapi import FastAPI

from app.routers.routerCard import router as routerCard
from app.routers.routerLottery import router as routerLottery
from app.routers.routerTransactionComing import router as routerTransComing

app = FastAPI(openapi_prefix="/api", title="API Lottery", version="1.0.0")

app.include_router(routerLottery)
app.include_router(routerCard)
app.include_router(routerTransComing)



if __name__ == '__main__':
    uvicorn.run(app='main:app', host="localhost", port=8000)

