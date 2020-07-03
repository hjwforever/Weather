import os

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

data = pd.read_csv('DataResult.csv', parse_dates=['date'])
dta = data['tmin']
dta_year = data['date']

# 得到开始和结束年份
begin_year = dta_year[0:1].dt.year  # index value
end_year = dta_year[-1:].dt.year

# 设置数据类型
dta = np.array(dta, dtype=np.float)
# 转换为Series类型的唯一数组
dta = pd.Series(dta)
dta.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))
dta.plot(figsize=(10, 6))

plt.savefig('test1.jpg')
plt.show()

# 一阶差分
fig = plt.figure(figsize=(6, 8))

ax0 = fig.add_subplot(411)
diff0 = dta.diff(0)
diff0.plot(ax=ax0)

ax1 = fig.add_subplot(412)
diff1 = dta.diff(1)
diff1.plot(ax=ax1)

ax2 = fig.add_subplot(413)
diff2 = dta.diff(2)
diff2.plot(ax=ax2)

ax3 = fig.add_subplot(414)
diff3 = dta.diff(3)
diff3.plot(ax=ax3)

plt.savefig('test2.jpg')
plt.show()

# ARIMA
diff1 = dta.diff(1)
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(dta, lags=30, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(dta, lags=30, ax=ax2)

plt.savefig('test3.jpg')
plt.show()

arma_mod76 = sm.tsa.ARMA(dta, (7, 6)).fit()
print(arma_mod76.aic, arma_mod76.bic, arma_mod76.hqic)

# 使用ARMA(7,6)
resid = arma_mod76.resid
fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=30, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=30, ax=ax2)

# 验证模型
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit=True)

plt.savefig('test4.jpg')
plt.show()

# 生成预测数据
# 未来10年同一天的预测数据
predict_year = 10
predict_end_year = end_year.values[0] + predict_year
predict_dta = arma_mod76.predict(str(end_year.values[0]), str(predict_end_year), dynamic=True)
print(predict_dta)
