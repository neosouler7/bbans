from manager.utils import read_config, get_current_time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self):
        self.mail_config = read_config().get("mail")

    def send_email(self, content):
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(self.mail_config.get("id"), self.mail_config.get("pwd"))

        msg = MIMEMultipart('alternative')

        msg['Subject'] = f'[BBANS] Daily News Issue ({get_current_time("%m/%d")})'
        msg['From'] = self.mail_config.get("id")
        msg['To'] = ",".join(self.mail_config.get("to"))
        msg['Cc'] = ",".join(self.mail_config.get("cc"))

        msg.attach(MIMEText(content, 'html', _charset='utf-8'))
        session.send_message(msg)
