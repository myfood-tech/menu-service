from fastapi import APIRouter

from src.models.menu import MenuBasic, MenuDBConnector

router = APIRouter(
    prefix="/menu",
    tags=["menu"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=MenuBasic)
async def read_menu(id: str):
    menu_example = MenuDBConnector.get_by_id(id)
    return menu_example