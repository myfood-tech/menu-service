from fastapi import FastAPI

from src.routers import menu, restaurant, admin

import os

if os.environ.get("STAGE", "") == "dev":
    alert_message = "–"*10 + "\n\n\n" + "ALERT!!!\n\nCURRENT MODE IS: DEV\n\n\n" + "–"*10 + "\n"
    print(alert_message)


description = """
my-food.tech API 🚀

## restaurant

Инфа о ресторанах. 
Некоторые методы закрыты или частично закрыты за админский токен.

## menu

Инфа о меню и блюдах. 
Некоторые методы закрыты или частично закрыты за админский токен.

## admin

Авторизация для админки
"""


app = FastAPI(
    title="my-food.tech API",
    description=description,
    version="0.0.1"
)

app.include_router(menu.router)
app.include_router(restaurant.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
