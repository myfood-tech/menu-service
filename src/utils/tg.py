import requests
import urllib.parse
import json
import os
import time


class TelegramAPI:
    def __init__(self):
        self.token = os.environ["TELEGRAM_TOKEN_AUTOMATION_BOT"]
        self.api_url = "https://api.telegram.org/bot"+self.token + "/"


# sending methods
    def send_message(self, chat_id, message, buttons=[], force_reply=False, input_field_placeholder="", silent=True):        
        message = urllib.parse.quote_plus(message)
        message_url = self.api_url + "sendMessage?chat_id=" + str(chat_id) + \
            "&text=" + message
        if silent:
            message_url += "&disable_notification=True"
        if force_reply:
            force_reply = {
                "force_reply" : True,
                "input_field_placeholder":  input_field_placeholder
            }
            message_url += "&reply_markup=" + json.dumps(force_reply)
        else:
            if len(buttons):
                # inline_keyboard
                #   text
                
                keybord_buttons = {}
                inline_keyboard = []
                for i,b in enumerate(buttons):
                    text = b["text"]
                    # print("TEXT: ", text)
                    # print(b.keys())
                    the_key = ""
                    for k in b.keys():
                        if not "text" in k:
                            the_key = k
                    the_key_data = b[k]
                    # print(the_key, the_key_data)
                    button_obj = {
                        'text' : urllib.parse.quote_plus(text),
                        the_key : urllib.parse.quote_plus(str(the_key_data))
                    }
                    inline_keyboard.append([button_obj])
                keybord_buttons = {
                    'inline_keyboard' : inline_keyboard
                }
                keybord_buttons = json.dumps(keybord_buttons)
                
                message_url += "&reply_markup=" + keybord_buttons
        # print("URL: ", message_url)
        x = requests.post(message_url)
        text = x.text
        body = json.loads(text)
        pretty = json.dumps(body, indent=4, sort_keys=True)
        # print(pretty)
        return body
