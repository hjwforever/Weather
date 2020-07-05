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
