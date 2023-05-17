import multiprocessing as mp

from manager.tg import Tg
from manager.commander import Commander
from manager.utils import read_config

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Main:
    def __init__(self):
        self.tg_config = read_config().get("tg")
        self.tg = Tg()
        self.commander = Commander()

    def run(self):
        start_msg = "## START bbans\n"
        print(start_msg)
        self.tg.send_message(start_msg)


        updater = Updater(token=self.tg_config.get("token"), use_context=True, workers=self.tg_config.get("workers"))
        dispatcher = updater.dispatcher

        whoami_handler = CommandHandler(['whoami'], self.commander.tg_whoami, pass_args=True, run_async=False)
        status_handler = CommandHandler(['status', 'st'], self.commander.tg_status, pass_args=True, run_async=False)
        send_handler = CommandHandler(['send', 's'], self.commander.tg_send, pass_args=True, run_async=False)

        error_handler = MessageHandler(Filters.text | Filters.command, self.commander.tg_error, run_async=False)

        dispatcher.add_handler(whoami_handler)
        dispatcher.add_handler(status_handler)
        dispatcher.add_handler(send_handler)

        dispatcher.add_handler(error_handler)

        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    m = Main()
    mp.set_start_method("fork")
    mp.Process(target=m.run, args=()).start()
