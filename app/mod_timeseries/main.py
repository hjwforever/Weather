from app.mod_timeseries.arimaMethod import ArimaMethod
from app.mod_timeseries.dataClean import DataClean
from datetime import datetime
from app.mod_timeseries.analyzeData import analyzeData
# cld= DataClean()
# cld.cleanData(startTime='1980-01-01', endTime='2020-12-31', isChooseDay=False,resultFileName='historyData.csv')

# p= ArimaMethod()
# p.predict(dataType='tmin', startTime='2010-03-01', endTime='2010-11-10', preDay='9')

q=analyzeData()
#用for循环输出1990前六年（默认5年）7月份平均最低温数据
for element in q.MonthTminData(1990,7,6):
    print(element)
for element in q.MonthTmaxData(1990,7):
    print(element)