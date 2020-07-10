import os, django
from threading import Timer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")  # project_name 项目名称
django.setup()
from app import models

import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import Weather.settings as settings
def send_mail(email,event,title="来自Six-Single-Dogs天气网站的定时提醒邮件"):
    # send_mail(title, content, settings.EMAIL_HOST_USER, "hjwbelieve@foxmail.com")
    text_content = """感谢注册！如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！"""
    content = "<p>您好，本站温馨提醒您在本站设置的近期日程安排事项如下:</p> "+event
    msg = EmailMultiAlternatives(title, text_content, settings.EMAIL_HOST_USER, ["hjwbelieve@foxmail.com"])
    msg.attach_alternative(content, "text/html")
    msg.send()

def task():
    datenow = timezone.now()
    memorandum = models.Memorandum.objects.filter().values()
    print(memorandum)
    for i in memorandum:
        if(i["time"]-datenow <=  datetime.timedelta(hours=2)):
            # print(datenow)
            # print(i["time"])
            # print(i["email"])
            # print(i["eventContent"])
            send_mail(i["email"], i["eventContent"])
            thememorandum = models.Memorandum.objects.filter(name=i["name"], time=i["time"], eventContent=i["eventContent"])
            thememorandum.delete()
            print('send reminder email to  "'+i["name"]+'"  "'+i["email"]+'", ok!')

    print('AMD.YES!')
    t = Timer(10, task)
    t.start()

if __name__ == '__main__':
    try:
        task()
    except (KeyboardInterrupt, SystemExit):
        pass
