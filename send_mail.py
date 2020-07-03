#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 16:23
# @Author  : ZhangChaowei
# @Site    : 
# @File    : send_mail.py
# @Software: PyCharm


import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'


if __name__ == '__main__':
    # send_mail(
    #     '来自Django的测试邮件',
    #     '欢迎学习Django，这里是邮件内容！',
    #     'richardojang@sina.com',  # 邮件发送方
    #     ['835272016@qq.com'],  # 接受方的邮件地址列表
    # )
    subject, form_email, to = '来自Django的测试邮件', 'richardojang@sina.com', '835272016@qq.com'
    text_content = '欢迎学习Django，这里是邮件内容！'
    html_content = '<p>欢迎访问<a href="http://www.baidu.com" target=blank>www.baidu.com</a>，Django技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, form_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



