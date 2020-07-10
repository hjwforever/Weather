import os, django
from itertools import chain

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")  # project_name 项目名称
django.setup()
import logging
import hashlib
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from datetime import datetime
from datetime import timedelta
from . import models
from . import forms
from Weather import settings
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import pandas as pd
import app.mod_timeseries.weather_model as wm
import numpy as np
from Weather import settings
# from app.static.weather_training import predict_dta as pdata
import json
from random import randrange
from rest_framework.views import APIView
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from app.models import Weather
from rest_framework.decorators import api_view
from django.utils import timezone
from django.core import serializers

# import os, django
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weather.settings")
# django.setup()
global city


class EventsForm(object):
    pass


def selectcity(request):
    print(request.session.get('is_login', None))
    if request.session.get('is_login', None):
        print('登录者姓名：')
        print(request.session['user_name'])
    print('嘿嘿嘿')
    city = request.GET.get('city')
    print(city)

    datenow = timezone.now()
    theday = datenow + timedelta(days=6)
    queryset = models.PredictData.objects.filter(date__range=[datenow, theday], city=city).order_by('date')

    data = serializers.serialize("json", queryset)
    queryset = json.loads(data)
    print('data:')
    print(data)
    # return JsonResponse(data, safe=False)
    print('queryset::::::::')
    print(queryset)
    return JsonResponse(queryset, json_dumps_params={'ensure_ascii': False}, safe=False)

def selecthistorycity(request):
    city = request.GET.get('city')
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    print(city)
    print(year+month+day)

    if year == '0':
        History_data = models.HistoryData.objects.filter(city=city).order_by('date')
    else:
        if month == '0':
            History_data = models.HistoryData.objects.filter(date__year=year,city=city).order_by('date')
        else:
            if day == '0':
                History_data = models.HistoryData.objects.filter(date__year=year, date__month=month,city=city).order_by('date')
            else:
                History_data = models.HistoryData.objects.filter(date__year=year, date__month=month, date__day=day,city=city).order_by('date')
    data = serializers.serialize("json", History_data)
    queryset = json.loads(data)
    print('data:')
    print(data)
    print('querysethistory')
    print(queryset)
    return JsonResponse(queryset, json_dumps_params={'ensure_ascii': False}, safe=False)




def model2jsonArr(data):
    rData = {}
    for p in data:
        p.__dict__.pop("_state")  # 除去'model、pk'
        rData.append(p.__dict__)
    return rData


def changechart(request):
    city = request.GET.get('city')
    print(city)
    # datenow=datetime(2020, 7, 8)
    # queryset = models.HistoryData.objects.filter(date__year=datenow.year,date__month=datenow.month,city=city).order_by('date')
    # print('queryset:')
    # print(queryset.values())

    datenow = timezone.now()
    theday = datenow + timedelta(days=6)
    predict_queryset = models.PredictData.objects.filter(date__range=[datenow, theday],city=city).order_by('date')

    datenow = timezone.now()
    # today = datetime.date.today()
    yesterday = datenow - timedelta(days=1)
    everyyeartodaystart = datetime(datenow.year - 10, 1, 1)
    everyyeartodayhistory = models.HistoryData.objects.filter(date__range=[everyyeartodaystart, yesterday],
                                                              date__month=datenow.month, date__day=datenow.day,
                                                              city=city).order_by('date')
    # queryset = predict_queryset|everyyeartodayhistory
    queryset = chain(everyyeartodayhistory, predict_queryset)
    data = serializers.serialize("json", queryset)
    aqueryset = json.loads(data)
    print(aqueryset)
    # data = model2jsonArr(findwell)
    # return JsonResponse(data, safe=False)
    return JsonResponse(aqueryset, json_dumps_params={'ensure_ascii': False}, safe=False)


def get_calendar(request):
    name = request.GET.get('name')
    print("calendar:")
    print(name)
    queryset = models.Memorandum.objects.filter(name=name).order_by('time')
    data = serializers.serialize("json", queryset)
    queryset = json.loads(data)
    print('calendar_data:')
    print(data)
    print('calendar_queryset')
    print(queryset)
    return JsonResponse(queryset, json_dumps_params={'ensure_ascii': False}, safe=False)


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def home_index(request):
    return render(request, 'app/home-index.html')


def beijingweather(request):
    return render(request, 'app/beijingweather.html')


def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["周一", "周二", "周三", "周四", "周五", "周六", "周日"])
            .add_yaxis("最高温", [randrange(50, 100) for _ in range(7)])
            .add_yaxis("最低温", [randrange(0, 50) for _ in range(7)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar", subtitle="by第三小组"))
            .dump_options_with_quotes()
    )
    return c


def line_base() -> Line:
    data_set = pd.read_csv("app/static/DataResult.csv")
    # p = wm.ProcessData("app/static/DataResult.csv", 10, 'min')
    data = data_set.values[:, :]
    date = []
    tmax = []
    tmin = []
    for row in data:
        date.append(row[0])
        tmax.append(row[1])
        tmin.append(row[2])

    c = (
        Line()
            .add_xaxis(date)
            .add_yaxis("最高温", tmax)
            .add_yaxis("最低温", tmin)
            .set_global_opts(title_opts=opts.TitleOpts(title="Line", subtitle="by第三小组"))
            .dump_options_with_quotes()
    )
    return c


class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(line_base()))


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("app/templates/app/line.html").read())


def home(request):
    return render(request, 'app/home.html')


def index(request):
    print('调用了一次index方法#######################################')
    datenow = timezone.now()
    queryset = models.HistoryData.objects.filter(date=datenow).values().order_by('date')
    print('queryset:')
    print(queryset)
    predict_queryset = models.PredictData.objects.all().order_by('date')
    print('predict_queryset:')
    print(predict_queryset)
    everyyeartodaystart = datetime(datenow.year - 10, 1, 1)
    everyyeartodayhistory = models.HistoryData.objects.filter(date__range=[everyyeartodaystart, datenow],
                                                              date__month=datenow.month,
                                                              date__day=datenow.day).order_by('date')
    print('everyyeartodayhistory:')
    print(everyyeartodayhistory)

    queryset = predict_queryset.filter(date__day=datenow.day).values().order_by('city')
    print('queryset:')
    print(queryset)

    if request.session.get('is_login', None):
        return render(request, 'app/index.html', {'queryset': queryset, 'predict_queryset': predict_queryset,
                                                  'everyyeartodayhistory': everyyeartodayhistory, 'has_login': True,
                                                  'login_user_name': request.session['user_name']})
    else:
        return render(request, 'app/index.html', {'queryset': queryset, 'predict_queryset': predict_queryset,
                                                  'everyyeartodayhistory': everyyeartodayhistory, 'has_login': False})

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
    date = []
    tmax = []
    tmin = []
    for row in data:
        date.append(row[0])
        tmax.append(row[1])
        tmin.append(row[2])
    return render(request, 'app/show_excel.html', {'test_data': test_data, 'date': date, 'tmax': tmax, 'tmin': tmin})


def show_data(request):
    data = pd.read_csv('app/static/DataResult.csv', 'app/static/DataResult.csv')
    predict_year = request.GET.get('predict_year', 10)
    data_type = request.GET.get('data_type', 'min')
    return render(request, "app/show_data.html", {"data": wm.ProcessData(request, data, predict_year, data_type).all()})


def upload_file(request):
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


def history_page(request):
    History_data = models.HistoryData.objects.all()
    print(History_data)
    return render(request, 'app/search-history.html', {'History_data': History_data})


# def transfer_history(request):
    # city = request.GET.get('CC')
    # year = request.GET.get('YYYY')
    # mon = request.GET.get('MM')
    # day = request.GET.get('DD')
    # print(city)
    # print(year)
    # print(mon)
    # print(day)
    # if year == '0':
    #     History_data = models.HistoryData.objects.filter().values()
    # else:
    #     if mon == '0':
    #         History_data = models.HistoryData.objects.filter(date__year=year).values()
    #     else:
    #         if day == '0':
    #             History_data = models.HistoryData.objects.filter(date__year=year, date__month=mon).values()
    #         else:
    #             History_data = models.HistoryData.objects.filter(date__year=year, date__month=mon,
    #                                                              date__day=day).values()
    # print(History_data)
    # return render(request, 'app/search-history.html')


def hash_code(s, salt=settings.SECRET_KEY):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    print(code)
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = "来自Django的测试的注册确认邮件"

    text_content = """感谢注册！如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！"""

    html_content = """
                    <p>感谢注册<a href="http://127.0.0.1:8000/app/confirm/?code={0}" target=blank>点击完成注册</a>，\</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{1}天！</p>
                    """.format(code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def login(request):
    print('进入login视图函数')
    if request.session.get('is_login', None):
        datenow = timezone.now()
        queryset = models.HistoryData.objects.filter(date=datenow).values()
        print('queryset:')
        print(queryset)
        predict_queryset = models.PredictData.objects.all()
        print('predict_queryset:')
        print(predict_queryset)
        everyyeartodaystart = datetime(datenow.year - 10, 1, 1)
        everyyeartodayhistory = models.HistoryData.objects.filter(date__range=[everyyeartodaystart, datenow],
                                                                  date__month=datenow.month, date__day=datenow.day)
        print('everyyeartodayhistory:')
        print(everyyeartodayhistory)
        return render(request, 'app/index.html',
                      {'has_login': True, 'queryset': queryset, 'predict_queryset': predict_queryset,
                       'everyyeartodayhistory': everyyeartodayhistory, 'login_user_name': request.session['user_name']})
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = '请检查填写内容!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'app/login.html', locals())

            if not user.has_confirmed:
                message = "该用户还未经过邮件确认！"
                return render(request, 'app/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                datenow = timezone.now()
                queryset = models.HistoryData.objects.filter(date=datenow).values()
                print('queryset:')
                print(queryset)
                predict_queryset = models.PredictData.objects.all()
                print('predict_queryset:')
                print(predict_queryset)
                everyyeartodaystart = datetime(datenow.year - 10, 1, 1)
                everyyeartodayhistory = models.HistoryData.objects.filter(date__range=[everyyeartodaystart, datenow],
                                                                          date__month=datenow.month,
                                                                          date__day=datenow.day)
                print('everyyeartodayhistory:')
                print(everyyeartodayhistory)
                return render(request, 'app/index.html',
                              {'has_login': True, 'login_user_name': user.name, 'queryset': queryset,
                               'predict_queryset': predict_queryset,
                               'everyyeartodayhistory': everyyeartodayhistory})
            else:
                message = '密码不正确!'
                return render(request, 'app/login.html', locals())

        else:
            return render(request, 'app/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'app/login.html', locals())


def register(request):
    # if request.session.get('is_login', None):
    #     return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写内容!"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = "两次输入的密码不同!"
                return render(request, 'app/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用户名已存在!"
                    return render(request, 'app/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = "该邮箱已经被注册!"
                    return render(request, 'app/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                return redirect('/app/login/')
        else:
            return render(request, 'app/register.html', locals())
    register_form = forms.RegisterForm()
    mes = "请上邮箱"
    return render(request, 'app/register.html', locals())


def logout(request):
    print('登出函数')
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'app/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.now()
    if now > c_time + timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = "您的邮件已经过期！请重新注册！"
        return render(request, 'app/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = "感谢确认，请使用账户登陆！"
        return render(request, 'app/confirm.html', locals())


def hjh_test(request):
    big_data = models.PredictData.objects.all()
    return render(request, 'app/hjhTest.html', {'Bigdata': big_data})
