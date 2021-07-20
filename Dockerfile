FROM python:3.9-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip config set global.index-url https://pypi.douban.com/simple
RUN pip config set install.trusted-host pypi.douban.com
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple --trusted-host pypi.doubanio.com
#RUN pip install requests==2.25.1
#RUN pip install Django==3.1.2
#RUN pip install numpy==1.19.5
#RUN pip install apscheduler==3.7.0
#RUN pip install beautifulsoup4==4.9.3
#RUN pip install django_recaptcha==2.0.6
#RUN pip install djangorestframework==3.12.4
#RUN pip install fjd==0.1.58
#RUN pip install matplotlib
#RUN pip install pandas
#RUN pip install Pillow==8.3.1
#RUN pip install pyecharts==1.9.0
#RUN pip install python_dateutil==2.8.2
#RUN pip install scipy
#RUN pip install statsmodels==0.12.2
#RUN pip install django-simple-captcha==0.5.14

# copy project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]