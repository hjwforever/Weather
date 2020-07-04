from app.mod_timeseries.arimaMethod import ArimaMethod

p= ArimaMethod()
p.predict(dataType='tmin', startTime='2010-05-01', endTime='2010-11-10', preDay='5')

