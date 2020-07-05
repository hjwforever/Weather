from app.mod_timeseries.arimaMethod import ArimaMethod
from app.mod_timeseries.dataClean import DataClean
from datetime import datetime

# cld= DataClean()
# cld.cleanData(startTime='1980-01-01', endTime='2020-12-31', isChooseDay=False,resultFileName='historyData.csv')

p= ArimaMethod()
p.predict(dataType='tmin', startTime='2010-03-01', endTime='2010-11-10', preDay='9')

