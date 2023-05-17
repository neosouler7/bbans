from manager.utils import read_config


class ChatGPT:
    def __init__(self):
        self.config = read_config()
        self.api_key = self.config.get("chatgpt").get("api_key")

    def raise_question(self):
        pass

    def ask_if_bad_news(self):
        self.raise_question()
        pass
