import pandas as pd
from datetime import datetime
from dateutil import parser

data_raw = pd.read_csv('2200704.csv',encoding='utf-8')

#转换列名称和类型
data_raw['date'] = data_raw['DATE'].apply(parser.parse)
#data_raw['prcp'] = data_raw['PRCP'].astype(float)
#data_raw['tavg'] = data_raw['TAVG'].astype(float)
data_raw['tmax'] = data_raw['TMAX'].astype(float)
data_raw['tmin'] = data_raw['TMIN'].astype(float)

#得到需要的列
#data = data_raw.loc[:, ['date','prcp','tavg','tmax','tmin']]
data = data_raw.loc[:, ['date','tmax','tmin']]

#过滤掉空值
#data = data[pd.Series.notnull(data['prcp'])&pd.Series.notnull(data['tavg'])&pd.Series.notnull(data['tmax'])&pd.Series.notnull(data['tmin'])]
data = data[pd.Series.notnull(data['tmax'])&pd.Series.notnull(data['tmin'])]

data = data[(data['date'] >= datetime(1980,1, 1)) & (data['date'] <= datetime(2020,6, 28))]

data.query("date.dt.day == 1 & date.dt.month == 7", inplace=True)

#写入新csv文件
data.to_csv('DataResult.csv',index=None)