from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

class Weather(models.Model):
    date = models.DateTimeField(primary_key=True)
    tmax = models.FloatField()
    tmin = models.FloatField()
    tavg = models.FloatField()

    def __str__(self):
        return str(self.date)



class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女")
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateField(auto_now=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ": " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

class HistoryData(models.Model):
    date = models.DateField(primary_key=True)
    tmin = models.FloatField()
    tmax = models.FloatField()
    tavg = models.FloatField()
    prcp = models.FloatField()

    def __str__(self):
        return str(self.date)

class PredictData(models.Model):
    date = models.DateField(primary_key=True)
    tmin = models.FloatField(null=True)
    tmax = models.FloatField(null=True)
    tavg = models.FloatField(null=True)
    prcp = models.FloatField(null=True)

    def __str__(self):
        return str(self.date)