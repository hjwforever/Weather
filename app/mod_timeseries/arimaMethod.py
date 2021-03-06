import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")# project_name 项目名称
django.setup()

import warnings
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pandas import DataFrame, Series
from app.mod_timeseries.dataClean import DataClean
from app import models
from datetime import datetime

class ArimaMethod:
    def __init__(self):
        pass

    def predict(self,cityName='beijing', dataType='tmin', startTime='1991-01-01', endTime='1991-12-31', preDay='01'):
        preSatrtYear = startTime[:4]
        trainStartYear = str(int(preSatrtYear) - 10)
        trainStartTime = trainStartYear + '-01-01'

        trainEndYear = str(int(preSatrtYear) - 1)
        trainEndTime = str(int(startTime[:4]) - 1) + '-12-31'

        print(startTime)
        print(endTime)
        # print(trainStartTime)
        # print(trainEndTime)

        cld= DataClean()
        if dataType=='tmin':
            cld.cleanData(cityName=cityName, startTime=str(trainStartTime), endTime=str(startTime), day=preDay,justNeedTmin=True)
        elif dataType=='tmax':
            cld.cleanData(cityName=cityName, startTime=str(trainStartTime), endTime=str(startTime), day=preDay, justNeedTmax=True)
        elif dataType=='tavg':
            cld.cleanData(cityName=cityName, startTime=str(trainStartTime), endTime=str(startTime), day=preDay, justNeedTavg=True)
        elif dataType=='prcp':
            cld.cleanData(cityName=cityName, startTime=str(trainStartTime), endTime=str(startTime), day=preDay, justNeedPrcp=True)


        # Defaults
        plt.rcParams['figure.figsize'] = (20.0, 10.0)
        plt.rcParams.update({'font.size': 12})
        plt.style.use('ggplot')

        # Load the data
        data = pd.read_csv('trainData.csv', engine='python', skipfooter=3, usecols=['date', dataType])#skipfooter=3,
        print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
        print(data)
        i = 0
        for ch in data['date'].values:
            data['date'].values[i]=ch[:-3]
            i=i+1

        #print(data['date'].values)
        # print(isinstance(data['date'], DataFrame))
        # print(data['date'])

        # A bit of pre-processing to make it nicer
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        data.set_index(['date'], inplace=True)

        print('MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')
        print(data)


        # Plot the data
        data.plot()
        plt.ylabel('history_'+dataType)
        plt.xlabel('date')
        plt.show()

        # Define the d and q parameters to take any value between 0 and 1
        q = d = range(0, 2)
        # Define the p parameters to take any value between 0 and 3
        p = range(0, 4)

        # Generate all different combinations of p, q and q triplets
        pdq = list(itertools.product(p, d, q))

        # Generate all different combinations of seasonal p, q and q triplets
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        print('Examples of parameter combinations for Seasonal ARIMA...')
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
        print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
        print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))


        # train_data = data[trainStartTime:trainEndTime]
        train_data = data[trainStartTime:startTime]                 #如果有问题就把这行换成上面一行
        #train_data = data['2002-01-01':'2011-12-31']
        test_data = data[startTime:endTime]

        warnings.filterwarnings("ignore")  # specify to ignore warning messages

        AIC = []
        SARIMAX_model = []

        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(train_data,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)

                    results = mod.fit()

                    print('SARIMAX{}x{} - AIC:{}'.format(param, param_seasonal, results.aic), end='\r')
                    AIC.append(results.aic)
                    SARIMAX_model.append([param, param_seasonal])
                except:
                    continue

            print(
                'The smallest AIC is {} for model SARIMAX{}x{}'.format(min(AIC), SARIMAX_model[AIC.index(min(AIC))][0],
                                                                       SARIMAX_model[AIC.index(min(AIC))][1]))

        # Let's fit this model
        mod = sm.tsa.statespace.SARIMAX(train_data,
                                        order=SARIMAX_model[AIC.index(min(AIC))][0],
                                        seasonal_order=SARIMAX_model[AIC.index(min(AIC))][1],
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)

        results = mod.fit()

        results.plot_diagnostics(figsize=(20, 14))
        plt.show()

        pred2 = results.get_forecast(endTime)
        pred2_ci = pred2.conf_int()
        print(pred2.predicted_mean[startTime:endTime])
        data2= pred2.predicted_mean[startTime:endTime]

        print(isinstance(data2, DataFrame))
        print(isinstance(data2, Series))
        # for row in data2.itertuples():

        for date_0, value in data2.iteritems():
            value = round(value)
            date = datetime(date_0.year, date_0.month, int(preDay))


            queryset = models.PredictData.objects.filter(date=date,city=cityName)
            if queryset.exists():
                if dataType=='tmin':
                    models.PredictData.objects.filter(date=date,city=cityName).update(tmin=value)
                elif dataType=='tmax':
                    models.PredictData.objects.filter(date=date,city=cityName).update(tmax=value)
                elif dataType=='tavg':
                    models.PredictData.objects.filter(date=date,city=cityName).update(tavg=value)
            else:
                if dataType=='tmin':
                    models.PredictData.objects.create(date=date, tmin=value,city=cityName)
                elif dataType=='tmax':
                    models.PredictData.objects.create(date=date, tmax=value,city=cityName)
                elif dataType=='tavg':
                    models.PredictData.objects.create(date=date, tavg=value,city=cityName)

        ax = data.plot(figsize=(20, 16))
        pred2.predicted_mean.plot(ax=ax, label='Dynamic Forecast (get_forecast)')
        ax.fill_between(pred2_ci.index, pred2_ci.iloc[:, 0], pred2_ci.iloc[:, 1], color='k', alpha=.1)
        plt.ylabel('history_'+dataType)
        plt.xlabel('Date')
        plt.legend()
        plt.show()

        # print(isinstance(data2, (dict, DataFrame)))
        # print(data2.keys)
        # print(data2.values)
        # i = 0
        # tailDay = startTime[8:]
        # for ch in data2.keys:
        #     data2.keys[i] = ch[:-3]
        #     data2.keys[i] = data2.keys[i] + tailDay
        #     i = i + 1
        #
        # print(data2)