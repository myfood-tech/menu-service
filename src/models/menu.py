# menu model
from typing import Union, Optional, List

from pydantic import BaseModel


class MenuItem(BaseModel):
    title: str
    description: Optional[str]
    image: Optional[str]
    is_stop: bool = False
    price: float
    gramms: Optional[int]
    additional: object = {}


class SubMenu(BaseModel):
    id: str
    name: str
    menu_items: List[MenuItem]


class MenuBasic(BaseModel):
    id: str
    name: str
    description: Optional[str]
    sub_menus: List[SubMenu]


class MenuDBStub():
    def __init__(self):
        midii = MenuItem(
            **{
                "title": "Мидии блю-чиз",
                "description": "Черноморские мидии в соусе блю-чиз. Подаются с хрустящим багетом.",
                "image": "https://my-food.tech/static/media/midii_blu.a0905c51d5bd48b33463.webp",
                "is_stop": False,
                "price": 990,
                "gramms": 300
            }
        )
        tom_yam = MenuItem(
            **{   
                "title": "Том Ям",
                "description": "Азиатский суп из морепродуктов. Подаётся вместе с рисом.",
                "image": "https://my-food.tech/static/media/tom_yam.f8dd28c51674e7f52a1b.jpeg",
                "is_stop": False,
                "price": 690,
                "gramms": 400
            }
        )
        beef_baran = MenuItem(
            **{
                "title": "Бифштекс из баранины",
                "image": "https://my-food.tech/static/media/beef_baran.4e3b0c59d238fa084c2e.webp",
                "is_stop": True,
                "price": 810,
                "gramms": 300
            }
        )
        beef_gov = MenuItem(
            **{
                "title": "Бифштекс из говядины",
                "image": "https://my-food.tech/static/media/beef_gov.328e424ab9924cf3f4a6.jpeg",
                "is_stop": False,
                "price": 700,
                "gramms": 300
            }
        )
        sub_menu_main = SubMenu(
            **{
                "id": "SubMenuID_123",
                "name": "Основное",
                "menu_items": [midii, tom_yam, beef_baran, beef_gov]
            }
        )

        chicken = MenuItem(
            **{
                "title": "Куриные крылья",
                "description": "С крудите и блю-чиз",
                "image": "https://my-food.tech/static/media/grilled_chicken.b168c20dbbb7a376168f.webp",
                "is_stop": False,
                "price": 550,
                "gramms": 350
            }
        )
        grenki = MenuItem(
            **{
                "title": "Гренки",
                "image": "https://my-food.tech/static/media/grenki.d6b042b413acb5858696.jpeg",
                "is_stop": False,
                "price": 550,
                "gramms": 350
            }
        )
        zakuski = SubMenu(
            **{
                "id": "SubMenuID_456",
                "name": "Закуски",
                "menu_items": [grenki, chicken]
            }
        )

        blanche = MenuItem(
            **{
                "title": "BLANCHE DE BRUXELLES",
                "description": "БЕЛЬГИЯ. Светлое пшеничное нефильтрованное. Плотность 18% | Алк.7%",
                "image": "https://my-food.tech/static/media/blanche.525491312bd532640082.png",
                "is_stop": False,
                "price": 380
            }
        )
        rouge = MenuItem(
            **{
                "title": "ROUGE DE BRUXELLES",
                "description": "БЕЛЬГИЯ. Вишневый эль. Аромат забродившей спелой. Плотность 18%| Алк.7%",
                "image": "https://my-food.tech/static/media/grenki.d6b042b413acb5858696.jpeg",
                "is_stop": False,
                "price": 450
            }
        )
        alko = SubMenu(
            **{
                "id": "SubMenuID_789",
                "name": "Алкоголь",
                "menu_items": [blanche, rouge]
            }
        )
        self.menu = MenuBasic(
            **{
                "id": "MenuID_123",
                "name": "Меню",
                "sub_menus": [sub_menu_main, zakuski, alko]
            }
        )

    def get_by_id(self, some_fake_id):
        return self.menu


MenuDBConnector = MenuDBStub()
