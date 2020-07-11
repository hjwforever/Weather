import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")# project_name 项目名称
django.setup()
from app import models
import datetime

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from apscheduler.schedulers.blocking import BlockingScheduler


def sendEmail(email='',title='您的日程提示',msg='',username=''):
    # 第三方 SMTP 服务
    mail_host = 'smtp.qq.com'  # 设置服务器
    mail_user = '1003964217@qq.com'  # 用户名
    mail_pass = 'gwkyiremkbqtbfdh'  # 口令

    sender = '1003964217@qq.com'
    receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("Six-Single-Dog天气网站", 'utf-8')
    message['To'] = Header("尊敬的用户"+username, 'utf-8')

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")

    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

def autoSendEmail():
    nowTime=datetime.datetime.now()
    twoOursLater=nowTime+datetime.timedelta(hours=+2)
    print(models.Memorandum.objects.filter(time__range=(nowTime,twoOursLater),hasRemind=False).values())
    for user in models.Memorandum.objects.filter(time__range=(nowTime,twoOursLater),hasRemind=False):
        msg="Six-Single-Dog天气网日程表提醒您：\n"+user.time.strftime("%Y-%m-%d %H:%M:%S")+"\n"+"待办："+user.eventContent
        sendEmail(email=user.email,msg=msg,username=user.name)
        models.Memorandum.objects.filter(name=user.name,id=user.id).update(hasRemind=True)


if __name__ == '__main__':
    autoSendEmail()
    scheduler = BlockingScheduler()
    scheduler.add_job(autoSendEmail, 'interval', minutes=30)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass