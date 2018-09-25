#!/usr/bin/env python
# coding: utf-8
# Date  : 2018-09-25 10:36:20
# Email : b4zinga@outlook.com
# Func  : python send email
# Refer : http://www.runoob.com/python3/python3-smtp.html

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server
mail_host = "smtp.exmail.qq.com"
mail_user = "xxxx@xxxx.cn"
mail_pass = "xxxxxxxxxxxxxxxxxxxxx"
mail_port = 465

sender = "xxxx@xxxx.cn"
receivers = ["xxxx@xxxxxn.cn"]

title = "SMTP Email Test"
content = """This is a SMTP Email Test"""

def sendEmail():
    """send email"""
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = '{}'.format(sender)
    message['To'] = ','.join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("Email bas been send successfully !")
    except smtplib.SMTPException as e:
        print(e)

def sendHtmlEmail():
    """send email with html"""
    content="""<p><a href="https://github.com/b4zinga/"> Click Me</a></p>"""
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = '{}'.format(sender)
    message['To'] = ','.join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("Email bas been send successfully !")
    except smtplib.SMTPException as e:
        print(e)

def sendAttachEmail():
    """send email with attachments"""
    message = MIMEMultipart()
    message['From'] = '{}'.format(sender)
    message['To'] = ','.join(receivers)
    message['Subject'] = title

    message.attach(MIMEText(content, 'plain', 'utf-8'))

    att1 = MIMEText(open(__file__, 'rb').read(), 'base64', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="send_email.py"'
    message.attach(att1)

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("Email bas been send successfully !")
    except smtplib.SMTPException as e:
        print(e)


def sendPicEmail():
    pass




if __name__ == '__main__':
    # sendEmail()
    # sendHtmlEmail()
    # sendAttachEmail()
    # sendPicEmail()