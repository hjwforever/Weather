import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")# project_name 项目名称
django.setup()
from app import models
from datetime import datetime
from app.mod_timeseries.arimaMethod import ArimaMethod
from app.mod_timeseries.dataClean import DataClean
from datetime import datetime
from app.mod_timeseries.analyzeData import analyzeData
from django.utils import timezone

from app.mod_timeseries.WebCrawler import *

# 删除所有历史数据（除非迫不得已不得调用）
# models.HistoryData.objects.filter().all().delete()

# 清洗数据并将数据存入数据库（非常耗时请勿随意调用）
# cld= DataClean()
# cld.cleanData(cityName='hailar',startTime='1980-01-01', endTime='2020-12-31', needAllData=True,isChooseDay=False,resultFileName='historyData.csv')

# print(models.HistoryData.objects.filter(date__year=1980, date__month=1,date__day=3).values())

# 预测未来天气
datenow = timezone.now()
# models.PredictData.objects.filter(date__year=datenow.year, date__month=datenow.month,date__day=datenow.day).delete()
# startTime = datetime(datenow.year,datenow.month,1).strftime("%Y-%m-%d")
# endTime=datetime(datenow.year,datenow.month+3,1).strftime("%Y-%m-%d")
#
# print(startTime)
# print(endTime)
#
# # i=datenow.day
# # i=i+3
# p= ArimaMethod()
# for i in range(datenow.day+1,datenow.day+7):
#     p.predict(cityName='longyan',dataType='tmin', startTime=startTime, endTime=endTime, preDay=str(i))


#爬取当天数据并存入数据库
# todayWeather = today_webCrawler(cityName='beijing')
# tavg=round((todayWeather[1]+todayWeather[0])/2)
# queryset = models.PredictData.objects.filter(date=datenow,city='beijing')
# if not queryset.exists():
#     models.PredictData.objects.create(city= 'beijing', date=datenow, tmax=todayWeather[1],tmin=todayWeather[0],tavg= tavg,weather=todayWeather[2])
# else:
#     queryset.update(tmax=todayWeather[1],tmin=todayWeather[0],tavg= tavg)

# 爬取七天数据
sevenDayWeatherSet=sevenDaywebCrawler(cityName='beijing')
print(sevenDayWeatherSet)
for weather in sevenDayWeatherSet:
    day=int(weather[0][:-5])
    print(day)
    q = models.PredictData.objects.filter(date__day=day, city='beijing')
    print(q)
    if q.exists():
        q.update(weather=weather[1])
        # models.PredictData.objects.filter(date__day=day, city='beijing').update(weather=weather[1])
        print(weather[1])








# data=models.HistoryData.objects.filter(date__year=2010, date__month=3).values()
# print(data)
# print(len(data))
# avg=0
# for x in data:
#     avg+=x['tmin']
#     print(x['tmin'])
# print(avg/len(data))
# q=analyzeData()
# #用for循环输出1990前六年（默认5年）7月份平均最低温数据
# for element in q.MonthTminData(1990,7,6):
#     print(element)
# for element in q.MonthTmaxData(1990,7):
#     print(element)