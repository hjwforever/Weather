from urllib.request import urlopen
from bs4 import BeautifulSoup

# http://www.weather.com.cn/weather/101010100.shtml北京
# http://www.weather.com.cn/weather/101030100.shtml天津
# http://www.weather.com.cn/weather/101180101.shtml郑州
# http://www.weather.com.cn/weather/101200201.shtml襄阳
# http://www.weather.com.cn/weather/101230701.shtml龙岩
# http://www.weather.com.cn/weather/101240510.shtml丰城
# http://www.weather.com.cn/weather/101081001.shtml海拉尔
# resp=urlopen('http://www.weather.com.cn/weather/101030100.shtml')
# soup=BeautifulSoup(resp,'html.parser')
# tagToday=soup.find('p',class_="tem")  #第一个包含class="tem"的p标签即为存放今天天气数据的标签
# try:
#     temperatureHigh=tagToday.span.string  #有时候这个最高温度是不显示的，此时利用第二天的最高温度代替。
# except AttributeError as e:
#     temperatureHigh=tagToday.find_next('p',class_="tem").span.string  #获取第二天的最高温度代替
#
# temperatureLow=tagToday.i.string  #获取最低温度
# weather=soup.find('p',class_="wea").string #获取天气
#
# print('最低温度:' + temperatureLow)
# print('最高温度:' + temperatureHigh)
# print('天气:' + weather)


def webCrawler(cityName='beijing'):
   if cityName == 'beijing':#北京
       cityCode = '101010100'
   if cityName == 'tianjin':#天津
       cityCode = '101030100'
   if cityName == 'zhengzhou':#郑州
       cityCode = '101180101'
   if cityName == 'xiangyang':#襄阳
       cityCode = '101200201'
   if cityName == 'longyan':#龙岩
       cityCode = '101230701'
   if cityName == 'fengcheng':#丰城
       cityCode = '101240510'
   if cityName == 'hailar':#海拉尔
       cityCode = '101081001'

   InfoSet = []
   resp=urlopen('http://www.weather.com.cn/weather/'+cityCode+'.shtml')
   soup=BeautifulSoup(resp,'html.parser')
   tagToday=soup.find('p',class_="tem")  #第一个包含class="tem"的p标签即为存放今天天气数据的标签
   try:
       temperatureHigh=tagToday.span.string  #有时候这个最高温度是不显示的，此时利用第二天的最高温度代替。
   except AttributeError as e:
       temperatureHigh=tagToday.find_next('p',class_="tem").span.string  #获取第二天的最高温度代替

   temperatureLow=tagToday.i.string  #获取最低温度
   weather=soup.find('p',class_="wea").string #获取天气
   print(cityName)
   # temperatureLow.replace('℃','1')
   # re.sub('℃','',temperatureLow)
   # type(temperatureLow) is types.StringType

   # if isinstance(temperatureLow, str):
   #     print('true')
   # else:
   #     print('其他类型')


   #将爬取的最低温中的‘℃’删去
   l = list(temperatureLow)
   l[2] = ''
   temperatureLow = ''.join(l)

   print('最低温度:' + temperatureLow)
   InfoSet.append(temperatureLow)
   print('最高温度:' + temperatureHigh)
   InfoSet.append(temperatureHigh)
   print('天气:' + weather)
   InfoSet.append(weather)
   return InfoSet#返回值为集合，0-最低温，1-最高温，2-天气


#函数调用方式
webCrawler('beijing')
print(webCrawler('beijing')[2])