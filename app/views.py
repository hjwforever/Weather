import logging

from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import pandas as pd
from app.num_count import _out_log
import app.mod_timeseries.weather_model as wm
from Weather import settings

class EventsForm(object):
    pass


def home(request):
     return render(request, 'app/home.html')


def login(request):
    return render(request, 'app/login.html')

def index(request):
    string = u"hhhhhhhhhhh"
    return render(request, 'app/index.html', {'string': string})

def get_test(request):
    data_set = pd.read_csv("app/static/DataResult.csv")
    p = wm.ProcessData("app/static/DataResult.csv", 10, 'min')
    data = data_set.values[:, :]
    test_data = []
    for row in data:
        ls = []
        for j in row:
            ls.append(j)
        test_data.append(ls)
    return render(request, 'app/show_excel.html', {'test_data': test_data})

def show_data(request):

    data = pd.read_csv('app/static/DataResult.csv', 'app/static/DataResult.csv')
    predict_year = request.GET.get('predict_year', 10)
    data_type = request.GET.get('data_type', 'min')
    return render(request, "show_data.htm", {"data": wm.ProcessData(request, data, predict_year, data_type).all()})

def upload_file(request):
    # def upload_csv(request):
    #     data = {}
    #     if "GET" == request.method:
    #         return render(request, "upload_file.html", data)
    #     # if not GET, then proceed
    #     try:
    #         csv_file = request.FILES["csv_file"]
    #         if not csv_file.name.endswith('.csv'):
    #             messages.error(request, 'File is not CSV type')
    #             return HttpResponseRedirect(reverse("myapp:upload_csv"))
    #         # if file is too large, return
    #         if csv_file.multiple_chunks():
    #             messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
    #             return HttpResponseRedirect(reverse("myapp:upload_csv"))
    #
    #         file_data = csv_file.read().decode("utf-8")
    #
    #         lines = file_data.split("\n")
    #         # loop over the lines and save them in db. If error , store as string and then display
    #         for line in lines:
    #             fields = line.split(",")
    #             data_dict = {}
    #             data_dict["name"] = fields[0]
    #             data_dict["start_date_time"] = fields[1]
    #             data_dict["end_date_time"] = fields[2]
    #             data_dict["notes"] = fields[3]
    #             try:
    #                 form = EventsForm(data_dict)
    #                 if form.is_valid():
    #                     form.save()
    #                 else:
    #                     logging.getLogger("error_logger").error(form.errors.as_json())
    #             except Exception as e:
    #                 logging.getLogger("error_logger").error(repr(e))
    #                 pass
    #
    #     except Exception as e:
    #         logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
    #         messages.error(request, "Unable to upload file. " + repr(e))
    #
    #     return HttpResponseRedirect(reverse("app/upload_csv"))
    if request.method == "POST":
        File = request.FILES.get("files", "app/static/DataResult.csv")
        predict_year = request.GET.get('predict_year', None)
        data_type = request.GET.get('data_type', None)
        if File is None:
            return HttpResponse("请选择需要上传的日志文件")
        else:
            with open("./app/upload_file/%s" % File.name, 'wb+') as  f:
                for chunk in File.chunks():
                    f.write(chunk)
        # return render(request, "upload_file.html", {"data": _out_log(request).all()})
        return render(request, "app/upload_file.html", {"files": File})
            # return render(request, "upload_file.html", {"data": ProcessData(request, File, predict_year, data_type).all()})
    else:
        return render(request, "app/upload_file.html")
