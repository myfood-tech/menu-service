# restaurant model
from typing import Union, Optional

from pydantic import BaseModel

from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os


class RestaurantBasic(BaseModel):
    name: str
    description: Optional[str]
    price_tag: Optional[str]
    logo_url: Optional[str]
    menu_id: Optional[str]  # Union[str, None] = None

class Restaurant(RestaurantBasic):
    id: str

class RestaurantForAdmin(Restaurant):
    owner: Union[object, None] = None

class RestaurantToAdd(RestaurantBasic):
    name: Optional[Union[str, None]] = None
    owner: Optional[Union[object, None]] = None #Union[object, None] = None


class RestaurantDBConnector():
    def __init__(self):
        self.__hostname = ""
        self.__username = ""
        self.__password = ""
        self.__database_name = "restaurants"
        self.__client = None
        self.__db = None
        self.__collection = None
        self.__load_secrets()
        self.__connect_to_db()

    
    def __load_secrets(self):
        load_dotenv("./secret_dbs.env")
        self.__hostname = os.environ.get("MONGODB_HOSTNAME", "Not_set")
        self.__username = os.environ.get("MONGODB_USERNAME", "Not_set")
        self.__password = os.environ.get("MONGODB_PASSWORD", "Not_set")
    

    def __connect_to_db(self):
        connection_str = f'mongodb://{self.__username}:{self.__password}@{self.__hostname}'
        self.__client = MongoClient(connection_str)

        self.__db = self.__client[self.__database_name]
        if self.__db.name != self.__database_name:
            raise "MongoDBConnectionError"
        self.__collection = self.__db["restaurant_collection"]
    
    def add_restaurant(self, restaurant_data):
        inserted = self.__collection.insert_one(restaurant_data.dict())
        inserted["id"] = inserted.pop("_id")
        return inserted
    
    def update_restaurant_by_id(self, id_rest, updated):
        self.__collection.replace_one(
            {"_id": ObjectId(id_rest)},
            updated,
        )

    def get_restaurants(self):
        restaurants = []
        for rest in self.__collection.find():
            rest["id"] = str(rest["_id"])
            rest_obj = RestaurantForAdmin(**rest)
            restaurants.append(rest_obj)
        return restaurants
    
    def get_restaurant_by_id(self, id_rest):
        restaurant = self.__collection.find_one({"_id": ObjectId(id_rest)})
        if restaurant is not None:
            restaurant["id"] = str(restaurant["_id"])
            restaurant = RestaurantForAdmin(**restaurant)
        return restaurant


RestaurantDB = RestaurantDBConnector()
