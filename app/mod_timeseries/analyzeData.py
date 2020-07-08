import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")# project_name 项目名称
django.setup()

from app import models

class analyzeData:

    def __init__(self):
        pass
    def MonthTminData(self,year=2010,month=3,gap=5):
        data = models.HistoryData.objects.filter(date__year=year, date__month=month).values()
        # print(data)
        # print(len(data))
        Monthdata = []

        for i in range(1, gap+1):
            data = models.HistoryData.objects.filter(date__year=year- i, date__month=month).values()
            avg = 0
            for x in data:
                avg += x['tmin']
            # print(len(data))
            # print(avg / len(data))
            Monthdata.append(int(avg / len(data)))

        return Monthdata

    def MonthTmaxData(self,year=2010,month=3,gap=5):
        data = models.HistoryData.objects.filter(date__year=year, date__month=month).values()
        # print(data)
        # print(len(data))
        Monthdata = []

        for i in range(1, gap+1):
            data = models.HistoryData.objects.filter(date__year=year- i, date__month=month).values()
            avg = 0
            for x in data:
                avg += x['tmax']
            # print(len(data))
            # print(avg / len(data))
            Monthdata.append(int(avg / len(data)))

        return Monthdata

    def avgMax(self):
        avgmax = ['' for i in range(12)]
        for i in range(12):
            avgmax[i] = 0
        for m in range(12):
            for y in range(1981, 2011):
                max = 0
                data = models.HistoryData.objects.filter(date__year=y, date__month=m + 1).values()
                for n in data:
                    max += n['tmax']
                avgmax[m] += max / len(data)
            avgmax[m] = avgmax[m] / 30
        return avgmax

    def avgMin(self):
        avgmin = ['' for i in range(12)]
        for i in range(12):
            avgmin[i] = 0
        for m in range(12):
            for y in range(1981, 2011):
                min = 0
                data = models.HistoryData.objects.filter(date__year=y, date__month=m + 1).values()
                for n in data:
                    min += n['tmin']
                avgmin[m] += min / len(data)
            avgmin[m] = avgmin[m] / 30
        return avgmin


    # def MonthTmaxData(self, year=2010, month=3,gap=5):
    #     data = models.HistoryData.objects.filter(date__year=year, date__month=month).values()
    #     # print(data)
    #     # print(len(data))
    #     Monthdata = []
    #
    #     for i in range(1, gap+1):
    #         data = models.HistoryData.objects.filter(date__year=year - i, date__month=month).values()
    #         avg = 0
    #         for x in data:
    #             avg += x['tmax']
    #         # print(len(data))
    #         # print(avg / len(data))
    #         Monthdata.append(avg / len(data))
    #
    #     return Monthdata
