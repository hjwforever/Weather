# from app.mod_timeseries.weather_model import ProcessData
# from app.mod_timeseries.weather_training import data

# p = ProcessData(data, 10, 'min')
# p.process_minmax()

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")# project_name 项目名称
django.setup()
from app import models
import datetime
from app.mod_timeseries.WebCrawler import *

today = datetime.date.today()
yestoday = today- datetime.timedelta(days=1)
tomorrow = today+ datetime.timedelta(days=1)

# # 补全预测数据中的平均温度
# for msg_0 in models.PredictData.objects.filter(date=tomorrow):
#     for msg in models.PredictData.objects.filter(city=msg_0.city):
#         models.PredictData.objects.filter(city=msg_0.city,date = msg.date).update(tavg=round((msg.tmax+msg.tmin)/2))


# for i in range(10, 16):
#
#     models.PredictData.objects.create(city='beijing',date=datetime.datetime(2020,7,i))


# # 爬取七天数据
# sevenDayWeatherSet=sevenDaywebCrawler(cityName='xiangyang')
# print(sevenDayWeatherSet)
# for weather in sevenDayWeatherSet:
#     day=int(weather[0][:-5])
#     print(day)
#     q = models.PredictData.objects.filter(date__day=day, city='xiangyang')
#     print(q)
#     if q.exists():
#         q.update(weather=weather[1])
#         # models.PredictData.objects.filter(date__day=day, city='beijing').update(weather=weather[1])
#         print(weather[1])

print(models.PredictData.objects.filter(city='beijing'))
print(models.PredictData.objects.filter(city='beijing').order_by('date'))