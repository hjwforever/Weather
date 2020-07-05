import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")# project_name 项目名称
django.setup()

import pandas as pd
from datetime import datetime
from dateutil import parser
from app import models
from pandas import DataFrame

class DataClean:
    def __init__(self):
        pass

    def cleanData(self, startTime ='', endTime ='',isChooseDay=True, day='',resultFileName='trainData.csv'):
        startYear = int(startTime[:4])
        startMonth = int(startTime[5:7])
        startDay = int(startTime[8:10])

        endYear = int(endTime[:4])
        endMonth = int(endTime[5:7])
        endDay = int(endTime[8:10])

        data_raw = pd.read_csv('originData.csv', encoding='utf-8')

        # 转换列名称和类型
        data_raw['date'] = data_raw['DATE'].apply(parser.parse)
        data_raw['prcp'] = data_raw['PRCP'].astype(float)
        data_raw['tavg'] = data_raw['TAVG'].astype(float)
        data_raw['tmax'] = data_raw['TMAX'].astype(float)
        data_raw['tmin'] = data_raw['TMIN'].astype(float)
        # data_raw['tavg'] = (data_raw['TMAX'].astype(float) + data_raw['TMIN'].astype(float))/2
        # 得到需要的列
        data = data_raw.loc[:, ['date','prcp','tavg','tmax','tmin']]
        #data = data_raw.loc[:, ['date', 'tmax', 'tmin', 'tavg']]

        # 过滤掉空值
        data = data[pd.Series.notnull(data['prcp'])&pd.Series.notnull(data['tavg'])&pd.Series.notnull(data['tmax'])&pd.Series.notnull(data['tmin'])]
        # data = data[pd.Series.notnull(data['tmax']) & pd.Series.notnull(data['tmin'])]

        data = data[(data['date'] >= datetime(startYear, startMonth, startDay)) & (data['date'] <= datetime(endYear, endMonth, endDay))]

        #data.query("date.dt.day == 1 & date.dt.month == 7", inplace=True)
        if isChooseDay:
            data.query("date.dt.day == "+ day, inplace=True)

        # 写入新csv文件
        data.to_csv(resultFileName, index=None)


        # data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        # print(data['date'].values)
        # print(data.values)
        print(isinstance(data, DataFrame))
        print('1111111111111111111111111111111111111111')
        print(data)
        # for msg in data['date']:
        #     print(msg)
        #     models.HistoryData.objects.create(date=msg,tavg=64,tmin=55,tmax=78,prcp=0.1)
        for row in data.itertuples():
            # print(getattr(row, 'c1'), getattr(row, 'c2'))  # 输出每一行
            # models.HistoryData.objects.

            models.HistoryData.objects.get_or_create(date=getattr(row, 'date'), tavg=getattr(row, 'tavg'), tmin=getattr(row, 'tmin'), tmax=getattr(row, 'tmax'), prcp=getattr(row, 'prcp'))