from typing import List, Union

from fastapi import APIRouter, Header, HTTPException

import os

from src.modules.admin_auth import AdminAuther

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token")
async def create_token(user_name):
    """
    # Создание временного админского токена для админа

    Метод присылает токен его владельцу в телегу
    """
    response_code = AdminAuther.create_token(user_name)
    if response_code != 200:
        raise HTTPException(status_code=response_code, detail="Token creation failed")
    return
