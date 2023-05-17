import datetime
import threading
import asyncio

from manager.tg import Tg
from manager.naver import Naver
from manager.chatgpt import ChatGPT
from manager.mail import Mail
from manager.utils import read_config, get_current_time, is_valid_date


class Commander:
    def __init__(self):
        self.tg = Tg()
        self.naver = Naver()
        self.chatgpt = ChatGPT()
        self.mail = Mail()
        self.config = read_config()
        self.tg_config = self.config.get("tg")
        self.mail_config = self.config.get("mail")

    def __log_and_notify(self, chat_id, func_name, log_msg, tg_msg):
        # tg_whoami 명령어 이외에는 commander만 수행 가능
        if func_name not in ["tg_whoami"]:
            if chat_id not in self.tg_config.get("chat_ids"):
                tg_msg = "you are not commander"

        print(f'{datetime.datetime.now()}|{func_name}|{log_msg}')
        print(f'{tg_msg}\n')
        self.tg.send_message(tg_msg)

    def tg_error(self, update, context):
        chat_id = update.message.chat_id
        log_msg = f'{chat_id}|{context.args}'

        # check input condition
        # None

        # process & send
        context.dispatcher.run_async(
            self.__log_and_notify,
            chat_id,
            'tg_error',
            log_msg,
            f'❗️no such command!\n',
            update=update
        )

    def tg_whoami(self, update, context):
        chat_id = update.message.chat_id
        log_msg = f'{chat_id}|{context.args}'

        # check if user is valid
        # None

        # process & send
        tg_msg = f'Hi, here is your tg ID : {chat_id}\n'
        context.dispatcher.run_async(
            self.__log_and_notify,
            chat_id,
            'tg_whoami',
            log_msg,
            f'{tg_msg}',
            update=update
        )

    def tg_status(self, update, context):
        chat_id = update.message.chat_id
        log_msg = f'{chat_id}|{context.args}'

        # check input condition
        # None

        # process & send
        tg_msg = f'## STATUS OK\n'

        context.dispatcher.run_async(
            self.__log_and_notify,
            chat_id,
            'tg_status',
            log_msg,
            f'{tg_msg}',
            update=update
        )

    def tg_send(self, update, context):
        chat_id = update.message.chat_id
        log_msg = f'{chat_id}|{context.args}'

        # check input condition
        if len(context.args) not in [1, 2]:
            tg_msg = f'❗️wrong format (ex. /send [start_date] [end_date(optional)])\n'
            context.dispatcher.run_async(
                self.__log_and_notify,
                chat_id,
                'tg_send',
                log_msg,
                f'{tg_msg}',
                update=update
            )
            return
        
        if len(context.args) == 1:
            start_date = context.args[0]
            end_date = start_date
        elif len(context.args) == 2:
            start_date, end_date = context.args[0], context.args[1]

        if not is_valid_date(start_date) or not is_valid_date(end_date):
            tg_msg = f'❗️wrong format (ex. /send 20230518, /send 20230518 20230520)\n'
            context.dispatcher.run_async(
                self.__log_and_notify,
                chat_id,
                'tg_send',
                log_msg,
                f'{tg_msg}',
                update=update
            )
            return
        
        # process & send
        tg_msg = f'crawling requested!\n'
        context.dispatcher.run_async(
            self.__log_and_notify,
            chat_id,
            'tg_send',
            log_msg,
            f'{tg_msg}',
            update=update
        )
        news_list = self.naver.crawl(start_date, end_date) # 네이버에 질의하여 기사 dict 의 array를 반환

        # TODO.
        # bad_news_list = self.chatgpt.ask_if_bad_news() # chatgpt에 질의하여 부정 기사 색출
        bad_news_list = news_list

        content, msg_common, msg_assemble, msg_group = f'', f'', f'', f''
        for b in bad_news_list:
            section = b.get("section")
            if section in ["common"]:
                msg_common += '<a href="{url}">{title}</a> ({publisher}, {published_at})<br>'.format(url=b.get("url"), 
                                                                                                     title=b.get("title"), 
                                                                                                     publisher=b.get("publisher"), 
                                                                                                     published_at=b.get("published_at"))
            elif section in ["assemble"]:
                msg_assemble += '<a href="{url}">[{keyword}] {title}</a> ({publisher}, {published_at})<br>'.format(url=b.get("url"), 
                                                                                                                   keyword=b.get("keyword"), 
                                                                                                                   title=b.get("title"), 
                                                                                                                   publisher=b.get("publisher"), 
                                                                                                                   published_at=b.get("published_at"))
            else:
                msg_group += '<a href="{url}">[{keyword}] {title}</a> ({publisher}, {published_at})<br>'.format(url=b.get("url"), 
                                                                                                                keyword=b.get("keyword"), 
                                                                                                                title=b.get("title"), 
                                                                                                                publisher=b.get("publisher"), 
                                                                                                                published_at=b.get("published_at"))
        content += f'[경영이슈]<br>'
        content += f'{msg_common}<br><br>'
        content += f'[완성차]<br>'
        content += f'{msg_assemble}<br><br>'
        content += f'[그룹사]<br>'
        content += f'{msg_group}<br><br>'

        print(content)
        
        tg_msg = f'no news to send :(\n'
        if len(content) > 0:
            threading.Thread(target=self.mail.send_email, args=(content,)).start()
            tg_msg = f'mail successfully sent :) \n'
        
        context.dispatcher.run_async(
            self.__log_and_notify,
            chat_id,
            'tg_send',
            log_msg,
            f'{tg_msg}',
            update=update
        )
