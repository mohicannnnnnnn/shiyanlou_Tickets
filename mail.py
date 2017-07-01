# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import pdb


class MyMail(object):
    Localmail = 'hggend@gmail.com'
    sendaddr = 'localhost'
    def __init__(self, emails, **email_info):
        self._emails = emails
        self._from = MyMail.Localmail
        if email_info:
            self._subject = email_info['subject']
            self._message = email_info['message']
        else:
            self._subject = 'None'
            self._message = 'None'

    def _construct_box(self):
        """construct a send mail box and return it"""
        send_msg = MIMEText(self._message, 'plain', 'utf-8')
        send_msg['From'] = Header('Hgg <%s>' % (self._from), 'utf-8')
        send_msg['To'] = Header('客户 <empty>', 'utf-8')
        send_msg['Subject'] = Header(self._subject, 'utf-8')
        return send_msg

    def send(self):
        """send mail"""
        send_message = self._construct_box()
        try:
            mysmtp = smtplib.SMTP(MyMail.sendaddr)
            mysmtp.sendmail(self._from, self._emails, send_message.as_string())
            print 'ok'
        except smtplib.SMTPException:
            print 'fail'

if __name__ == '__main__':
    print 'start'
    send_list = ['849709542@qq.com', '383728067@qq.com']
    msg = """
    明天开始做一个幸福的人, 我有一所大风案子, 拉拉
    """
    mail = MyMail(send_list, subject='你好, 简单的测试', message='测试成功')
    mail.send()

