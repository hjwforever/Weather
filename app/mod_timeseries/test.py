from app.mod_timeseries.weather_model import ProcessData
from app.mod_timeseries.weather_training import data

p = ProcessData(data, 10, 'min')
p.process_minmax()
