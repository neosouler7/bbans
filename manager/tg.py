import telegram
import datetime

from manager.utils import read_config
from telegram.utils.request import Request

MAX_MSG_LENGTH = 4096


class Tg:
    def __init__(self):
        self.tg_config = read_config().get("tg")
        self.bot = telegram.Bot(
            token=self.tg_config.get("token"), 
            request=Request(con_pool_size=self.tg_config.get("conn_pool"))
        )

    def send_message(self, chat_ids, message):
        message += f'\n{datetime.datetime.now()}'

        # short mesage
        q = len(message) // MAX_MSG_LENGTH
        if q == 0:
            for chat_id in self.tg_config.get("chat_ids"):
                self.bot.send_message(chat_id, message, timeout=1)
                return

        # long message
        for chat_id in self.tg_config.get("chat_ids"):
            for i in range(q):
                self.bot.send_message(
                    chat_id, message[MAX_MSG_LENGTH*i:MAX_MSG_LENGTH*(i+1)], timeout=1)
            self.bot.send_message(
                chat_id, message[MAX_MSG_LENGTH*q:], timeout=1)
