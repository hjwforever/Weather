import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")  # project_name 项目名称
django.setup()
from app import models

import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

from app.mod_timeseries.WebCrawler import *
from django.utils import timezone
from app.mod_timeseries.arimaMethod import ArimaMethod


def tick():
    today = datetime.date.today()
    yestoday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    # datenow = timezone.now()
    print('Tick! The time is: %s' % datetime.datetime.now())

    # 爬取当天数据并存入数据库
    print('爬取当天数据存入数据库...')
    for msg_0 in models.PredictData.objects.filter(date=tomorrow):
        todayWeather = today_webCrawler(cityName=msg_0.city)
        tavg = round((todayWeather[1] + todayWeather[0]) / 2)
        queryset_0 = models.PredictData.objects.filter(date=today, city=msg_0.city)
        if not queryset_0.exists():
            models.PredictData.objects.create(city=msg_0.city, date=today, tmax=todayWeather[1], tmin=todayWeather[0],
                                              tavg=tavg, weather=todayWeather[2])
        else:
            queryset_0.update(tmax=todayWeather[1], tmin=todayWeather[0], tavg=tavg, weather=todayWeather[2])
        queryset = models.HistoryData.objects.filter(date=today, city=msg_0.city)
        if not queryset.exists():
            models.HistoryData.objects.create(city=msg_0.city, date=today, tmax=todayWeather[1], tmin=todayWeather[0],
                                              tavg=tavg, weather=todayWeather[2])
        else:
            queryset.update(tmax=todayWeather[1], tmin=todayWeather[0], tavg=tavg, weather=todayWeather[2])
    print('爬取当天数据完成')

    # 如果预测数据表中存在昨日天气则删除
    if models.PredictData.objects.filter(date=yestoday).exists():
        models.PredictData.objects.filter(date=yestoday).delete()
        print('删除预测天气数据表中的昨日天气完成')

    # 预测未来第七天的天气
    print('开始预测未来七天天气')
    startTime = datetime.datetime(today.year, today.month, 1).strftime("%Y-%m-%d")
    endTime = datetime.datetime(today.year, today.month, 1).strftime("%Y-%m-%d")

    p = ArimaMethod()
    for msg_0 in models.PredictData.objects.filter(date=tomorrow):
        p.predict(cityName=msg_0.city, dataType='tmax', startTime=startTime, endTime=endTime, preDay=str(today.day + 6))
        p.predict(cityName=msg_0.city, dataType='tmin', startTime=startTime, endTime=endTime, preDay=str(today.day + 6))
    print('未来七天前期预测完成')

    # 补全预测数据中的平均温度
    print('补全预测数据中的平均温度')
    for msg_0 in models.PredictData.objects.filter(date=tomorrow):
        for msg in models.PredictData.objects.filter(city=msg_0.city):
            models.PredictData.objects.filter(city=msg_0.city, date=msg.date).update(tavg=round((msg.tmax + msg.tmin) / 2))
    print('补全预测数据中的平均温度结束')

    # 爬取七天数据更新天气状况
    print('爬取七天数据更新天气状况')
    for msg_0 in models.PredictData.objects.filter(date=tomorrow):
        sevenDayWeatherSet = sevenDaywebCrawler(cityName=msg_0.city)
        for weather in sevenDayWeatherSet:
            day = int(weather[0][:-5])
            q = models.PredictData.objects.filter(date__day=day, city=msg_0.city)
            if q.exists():
                q.update(weather=weather[1])
    print('爬取七天数据更新天气状况')
    print('自动预测结束，等待下一次预测...')

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'cron', hour=8, minute=55)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
