from dotenv import load_dotenv
import os
import hashlib
import time

from src.utils.tg import TelegramAPI


class AdminAuth():
    def __init__(self,):
        self.__TOKEN_STORAGE_RAM = {}
        self.__VALID_USERS = {}
        self.__load_users()
    
    def __load_users(self):
        load_dotenv("./secret_users.env")
        load_dotenv("./secret.env")

        super_admins_username = os.environ.get("SUPER_ADMINS", "[]")
        super_admins_username = super_admins_username.split(",")
        super_admins_chat_ids = os.environ.get("SUPER_ADMINS_TG", "[]")
        super_admins_chat_ids = super_admins_chat_ids.split(",")
        super_admins = {}
        for (un, chat_id) in zip(super_admins_username, super_admins_chat_ids):
            super_admins[un] = {
                "user_name": un,
                "chat_id": chat_id
            }
        
        
        admins_username = os.environ.get("ADMINS", "[]")
        admins_username = admins_username.split(",")
        admins_chat_ids = os.environ.get("ADMINS_TG", "[]")
        admins_chat_ids = admins_chat_ids.split(",")
        admins = {}
        for (un, chat_id) in zip(admins_username, admins_chat_ids):
            admins[un] = {
                "user_name": un,
                "chat_id": chat_id
            }
        self.__VALID_USERS["super_admins"] = super_admins
        self.__VALID_USERS["admins"] = admins
    

    def check_and_drop(self, user_name):
        if user_name in self.__TOKEN_STORAGE_RAM:
            token_data = self.__TOKEN_STORAGE_RAM[user_name]
            current_time = time.monotonic()
            if "creation_time" in token_data:
                if (current_time - token_data["creation_time"]) > token_data["timeout"]:
                    self.__TOKEN_STORAGE_RAM[user_name] = {}


    def find_user(self, user_name):
        for key in self.__VALID_USERS:
            if user_name in self.__VALID_USERS[key]:
                return self.__VALID_USERS[key][user_name]
        return None

    def create_token(self, user_name, timeout=30): #86_400
        user_data = self.find_user(user_name)
        if user_data is None:
            return 403
        self.check_and_drop(user_name)
        # token generation
        to_token = user_name + str(timeout) + str(time.monotonic())
        generated_token = hashlib.sha256(to_token.encode('utf-8')).hexdigest()
        # отправка токена в телегу
        chat_id = user_data["chat_id"] 
        message = f"Токен авторизации:\n{generated_token}"
        body_resp = TelegramAPI().send_message(chat_id, message)
        if body_resp.get("ok", "Error") != True:
            return 500

        # success -> saving token

        token_data = {
            "token": generated_token,
            "timeout": timeout,
            "creation_time": time.monotonic()
        }
        self.__TOKEN_STORAGE_RAM[user_name] = token_data

        return 200
    

    def check_token(self, user_name, token):
        self.check_and_drop(user_name)
        token_data = self.__TOKEN_STORAGE_RAM.get(user_name, {})
        if "token" in token_data:
            if token == token_data["token"]:
                return 200
            return 401
        return 403


AdminAuther = AdminAuth()
