import pandas as pd
from datetime import datetime
from dateutil import parser

class DataClean:
    def __init__(self):
        pass

    def cleanData(self, startTime ='', endTime ='', day=''):
        startYear=int(startTime[:4])
        startMonth= int(startTime[6:7])
        startDay= int(startTime[9:10])

        endYear = int(endTime[:4])
        endMonth = int(endTime[6:7])
        endDay = int(endTime[9:10])

        data_raw = pd.read_csv('historyData.csv', encoding='utf-8')

        # 转换列名称和类型
        data_raw['date'] = data_raw['DATE'].apply(parser.parse)
        # data_raw['prcp'] = data_raw['PRCP'].astype(float)
        data_raw['tavg'] = data_raw['TAVG'].astype(float)
        data_raw['tmax'] = data_raw['TMAX'].astype(float)
        data_raw['tmin'] = data_raw['TMIN'].astype(float)
        # data_raw['tavg'] = (data_raw['TMAX'].astype(float) + data_raw['TMIN'].astype(float))/2
        # 得到需要的列
        # data = data_raw.loc[:, ['date','prcp','tavg','tmax','tmin']]
        data = data_raw.loc[:, ['date', 'tmax', 'tmin', 'tavg']]

        # 过滤掉空值
        # data = data[pd.Series.notnull(data['prcp'])&pd.Series.notnull(data['tavg'])&pd.Series.notnull(data['tmax'])&pd.Series.notnull(data['tmin'])]
        data = data[pd.Series.notnull(data['tmax']) & pd.Series.notnull(data['tmin'])]

        data = data[(data['date'] >= datetime(startYear, startMonth, startDay)) & (data['date'] <= datetime(endYear, endMonth, endDay))]

        #data.query("date.dt.day == 1 & date.dt.month == 7", inplace=True)
        data.query("date.dt.day == "+ day, inplace=True)

        # 写入新csv文件
        data.to_csv('DataResult.csv', index=None)