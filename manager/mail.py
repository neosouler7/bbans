from manager.utils import read_config

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self):
        self.mail_config = read_config().get("mail")

    def send_email(self, title, content, target_list, mode):
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(self.mail_config.get("id"), self.mail_config.get("pwd"))

        for target in target_list:
            msg = MIMEMultipart('alternative')

            msg['Subject'] = title
            msg['From'] = self.mail_config.get("id")
            msg['To'] = target
            # if mode == "prd": # prd 일 경우 관리자 숨참
            #     msg['Bcc'] = ",".join(self.admin_list)

            msg.attach(MIMEText(content, 'html', _charset='utf-8'))
            session.send_message(msg)
