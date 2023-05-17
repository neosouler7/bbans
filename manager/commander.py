import datetime
import threading

from manager.tg import Tg
from manager.naver import Naver
from manager.chatgpt import Chatgpt
from manager.utils import read_config, get_current_time


class Commander:
    def __init__(self):
        self.tg = Tg()
        self.naver = Naver()
        self.chatgpt = Chatgpt()
        self.config = read_config()
        self.tg_config = self.config.get("tg")

    def __log_and_notify(self, chat_id, func_name, log_msg, tg_msg):
        # tg_whoami 명령어 이외에는 commander만 수행 가능
        if func_name not in ["tg_whoami"]:
            if commander not in self.tg_config.get("chat_ids"):
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
        tg_msg = f'Hi, here is your tg ID : {chat_id}'
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
        # TODO.
        # 네이버에 질의하여 기사 dict 의 array를 반환
        news_list = self.naver.crawl()

        # chatgpt에 질의하여 부정 기사 색출
        bad_news_list = self.chatgpt.ask_if_bad_news()
        
        # 최종 포맷팅하여 전달
        tg_msg = f''
        for news in bad_news_list:
            # TODO. 경영이슈, 완성차, 그룹사 묶기
            tg_msg += f'[ㅇㅇㅇ] ㅇㅇㅇㅇ (ㅇㅇㅇ, ㅇㅇㅇ)'


        chat_id = update.message.chat_id
        log_msg = f'{chat_id}|{context.args}'

        # check input condition
        if len(context.args) != 2:
            tg_msg = f'❗️wrong format (ex. /send [id] [test/prd])\n'
            context.dispatcher.run_async(
                self.__log_and_notify,
                chat_id,
                'tg_send',
                log_msg,
                f'{tg_msg}',
                update=update
            )
            return
        
        id = context.args[0]
        mode = context.args[1]
        member = self.config.get("member")
        member_id_list = [x.get("id") for x in member]
        if id != "all" and id not in member_id_list:
            tg_msg = f'❗️{id} not in member ({",".join(member_id_list)})\n'
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
        target, send_list = list(), list()
        if id == "all":
            target = member
        else:
            for m in member:
                if m.get("id") == id:
                    target.append(m)
                    break

        title = f'[fishingboat-{id}] 주간 수익 레포트 ({get_current_time("%Y/%m/%d")})'
        for m in target:
            if m.get("is_valid") == "Y":
                id = m.get("id")
                print(f'{id} mail sending ...')

                send_list.append(id)
                content = self.gspread.create_report(m)

                email_list = m.get("email_list")
                if mode == "test":
                    email_list = read_config().get("admin") # test 일 경우 관리자로 바꿔치기

                threading.Thread(target=self.mail.send_email, args=(title, content, email_list, mode,)).start()
        
        tg_msg = f'no member to send :(\n'
        if len(send_list) > 0:
            tg_msg = f'mail successfully sent :) \n→ {",".join(send_list)}\n'
        
        context.dispatcher.run_async(
            self.__log_and_notify,
            chat_id,
            'tg_send',
            log_msg,
            f'{tg_msg}',
            update=update
        )
    