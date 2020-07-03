from django.db import models

# Create your models here.
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()

class Weather(models.Model):
    name = models.CharField(max_length=30)
    tmax = models.FloatField()
    tmin = models.FloatField()
    tavg = models.FloatField()

