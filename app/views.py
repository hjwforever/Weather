import logging
import datetime
import hashlib
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from . import models
from . import forms
from Weather import settings
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import pandas as pd
from app.num_count import _out_log
import app.mod_timeseries.weather_model as wm
from Weather import settings
from app.static.weather_training import predict_dta as pdata

class EventsForm(object):
    pass


def home(request):
    l = pdata.values
    l2 = ['{:.2f}'.format(i) for i in l]
    dta = zip(pdata.keys(), l2)
    print(dta)
    return render(request, 'app/home.html', {'pdata': dta})


def login(request):
    return render(request, 'app/login.html')


def index(request):
    string = u"hhhhhhhhhhh"
    if not request.session.get('is_login', None):
        return redirect('/app/login/')
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


def history_page(request):
    data_set = pd.read_csv("app/static/DataResult.csv")
    p = wm.ProcessData("app/static/DataResult.csv", 10, 'min')
    data = data_set.values[:, :]
    test_data = []
    for row in data:
        ls = []
        for j in row:
            ls.append(j)
        test_data.append(ls)
    return render(request, 'app/history_data.html', {'test_data': test_data})


def hash_code(s, salt=settings.SECRET_KEY):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    print(code)
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = "来自Django的测试的注册确认邮件"

    text_content = """感谢注册！如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！"""

    html_content = """
                    <p>感谢注册<a href="http://{0}/app/confirm/?code={1}" target=blank>点击完成注册</a>，\
                    这里是Django学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{2}天！</p>
                    """.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def login(request):
    print('进入login视图函数')
    if request.session.get('is_login', None):
        return redirect('/index/')
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
                return redirect('/index/')
            else:
                message = '密码不正确!'
                return render(request, 'app/login.html', locals())

        else:
            return render(request, 'app/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'app/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

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
    return render(request, 'app/register.html', locals())

def logout(request):
    print('登出函数')
    if not request.session.get('is_login', None):
        return redirect('/app/login/')
    request.session.flush()
    return redirect('/app/login/')

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'app/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = "您的邮件已经过期！请重新注册！"
        return render(request, 'app/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = "感谢确认，请使用账户登陆！"
        return render(request, 'app/confirm.html', locals())
