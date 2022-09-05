from typing import List, Union

from fastapi import APIRouter, Header, HTTPException, Depends

import os

from src.routers.dependencies.auth import (
    check_username_token_header,
    check_username_token_header__return_status
)
from src.models.restaurant import Restaurant, RestaurantToAdd, RestaurantForAdmin, RestaurantDB

router = APIRouter(
    prefix="/restaurant",
    tags=["restaurant"],
    responses={404: {"description": "Not found"}},
)


@router.get("/all", dependencies=[Depends(check_username_token_header)])
async def read_all_restaurants():
    """
    # Метод закрыт за админскую авторизацию
    """
    rests = RestaurantDB.get_restaurants()
    return rests


@router.get("/")
async def read_restaurant_by_id(id_rest: str, token_validation: bool = Depends(check_username_token_header__return_status)):
    """
    # Метод  *частично* закрыт за админскую авторизацию:
    
    ***Частично закрыт это***:
    * с токеном будет полная инфа
    * без токена достаточная для пользователя
    """
    if len(id_rest) != 24:
        raise HTTPException(status_code=400, detail="ID must be length of 24 symbols")
    rest = RestaurantDB.get_restaurant_by_id(id_rest)
    if token_validation != 200:
        rest = Restaurant(**rest.dict())
    if rest is None:
        raise HTTPException(status_code=404, detail="No such restaurant found")
    return rest


@router.put("/")
async def update_restaurant_by_id(id_rest: str, update_fields: RestaurantToAdd, token_validation: bool = Depends(check_username_token_header)):
    """
    # Метод  закрыт за админскую авторизацию:

    Обновляет данные ресторана по id_rest
    """
    if len(id_rest) != 24:
        raise HTTPException(status_code=400, detail="ID must be length of 24 symbols")
    rest = RestaurantDB.get_restaurant_by_id(id_rest)
    if rest is None:
        raise HTTPException(status_code=404, detail="No such restaurant found")
    updated_version_stock = RestaurantToAdd(**rest.dict()).dict()
    updated_version = updated_version_stock.copy()

    update_fields_dict = update_fields.dict()
    for key in update_fields_dict:
        if update_fields_dict[key] is not None:
            updated_version[key] = update_fields_dict[key]
    if updated_version != updated_version_stock:
        # вот тут уже можно и обновлять
        updated_version = RestaurantToAdd(**updated_version)
        RestaurantDB.update_restaurant_by_id(id_rest, updated_version.dict())
        return updated_version
    else:
        raise HTTPException(status_code=400, detail="No field to update")
    


@router.post("/", dependencies=[Depends(check_username_token_header)])
async def create_restaurant(rest: RestaurantToAdd):
    """
    # Метод закрыт за админскую авторизацию
    """
    # get restaurant info from body
    # post it to mongoDB
    res = RestaurantDB.add_restaurant(rest)
    print(res)
    return res
