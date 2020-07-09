# encoding:utf-8
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def webCrawler(cityName='beijing', startYear=2011, endYear=2012):
    urls = []
    for year in range(startYear, endYear+1):
        for month in range(1,13):
            if month>=10:
                ur = 'http://lishi.tianqi.com/'+cityName+'/'+str(year) + str(month) + '.html'
            else:
                ur = 'http://lishi.tianqi.com/'+cityName+'/' + str(year) + '0'+str(month) + '.html'
            urls.append(ur)

    file = open(cityName+'_orgin_weather_data.csv', 'w', encoding='gbk')
    file.write('city,date,tmax,tmin,tavg\n')
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Cookie': 'cityPy=tianjin; cityPy_expire=1561950588; UM_distinctid=17133bbc7e6685-0b6045e36118e6-4313f6a-144000-17133bbc7e7a8e; CNZZDATA1275796416=1819259675-1585710340-%7C1585715624; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1585710877,1585712908,1585712984,1585716742; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1585716834'
    }
    for url in urls:
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_list = soup.select('div[class="tian_three"]')
        # print(weather_list)

        for weather in weather_list:
            weather_date = weather.select('ul[class="thrui"]')

            ul_list = weather.select('li')
            for ul in ul_list:
                li_list = ul.select('div')
                msg = ""
                msg = msg + cityName + ','
                msg = msg + li_list[0].string[:-5] + ','
                msg = msg + li_list[1].string[:-1] + ','
                msg = msg + li_list[2].string[:-1] + ','
                msg = msg + str(round((int(li_list[1].string[:-1]) + int(li_list[2].string[:-1])) / 2))

                if (msg != ' '):
                    file.write(msg + '\n')

    file.close()


# webCrawler(cityName='hulunbeier', startYear=2011, endYear=2020)


def today_webCrawler(cityName='beijing'):
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
   InfoSet.append(int(temperatureLow))
   print('最高温度:' + temperatureHigh)
   InfoSet.append(int(temperatureHigh))
   print('天气:' + weather)
   InfoSet.append(weather)
   return InfoSet#返回值为集合，0-最低温，1-最高温，2-天气


# 爬取未来七天天气
def get_page(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url,headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '错误'

def parse_page(html, return_list):
    soup = BeautifulSoup(html, 'html.parser')
    day_list = soup.find('ul', 't clearfix').find_all('li')
    for day in day_list:
        date = day.find('h1').get_text()
        wea = day.find('p',  'wea').get_text()
        if day.find('p', 'tem').find('span'):
                hightem = day.find('p', 'tem').find('span').get_text()
        else:
                hightem = ''
        lowtem = day.find('p', 'tem').find('i').get_text()
        # 将爬取的最低温中的‘℃’删去
        l = list(lowtem)
        l[2] = ''
        lowtem = ''.join(l)
        #win = re.search('(?<= title=").*?(?=")', str(day.find('p','win').find('em'))).group()
        win = re.findall('(?<= title=").*?(?=")', str(day.find('p','win').find('em')))
        wind = '-'.join(win)
        level = day.find('p', 'win').find('i').get_text()
        return_list.append([date, wea, lowtem, hightem, wind, level])
    #return return_list

def print_res(return_list):
    tplt = '{0:<10}\t{1:^10}\t{2:^10}\t{3:{6}^10}\t{4:{6}^10}\t{5:{6}^5}'
    print(tplt.format('日期', '天气', '最低温', '最高温', '风向', '风力',chr(12288)))
    for i in return_list:
        print(tplt.format(i[0], i[1],i[2],i[3],i[4],i[5],chr(12288)))
        print(i[0])
        print(i[1])



def sevenDaywebCrawler(cityName='beijing'):
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
   url = 'http://www.weather.com.cn/weather/'+cityCode+'.shtml'
   html = get_page(url)
   wea_list = []
   parse_page(html, wea_list)
   print_res(wea_list)
   return wea_list
