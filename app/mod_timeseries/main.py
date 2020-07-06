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

# cld= DataClean()
# cld.cleanData(startTime='1980-01-01', endTime='2020-12-31', needAllData=True,isChooseDay=False,resultFileName='historyData.csv')

models.PredictData.objects.all().delete()
datenow = timezone.now()
startTime = datenow.strftime("%Y-%m-%d")
endTime=datetime(datenow.year,datenow.month+1,1).strftime("%Y-%m-%d")

i=datenow.day
p= ArimaMethod()
for n in range(0,7):
    i=i+1
    p.predict(dataType='tavg', startTime=startTime, endTime=endTime, preDay=str(i))

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