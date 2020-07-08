# encoding:utf-8
import requests
from bs4 import BeautifulSoup

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
