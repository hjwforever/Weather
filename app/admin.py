from django.contrib import admin
from . import models
from app.models import *
# Register your models here.


# admin.site.register(models.User)
# admin.site.register(models.ConfirmString)
admin.site.register(HistoryData)
admin.site.register(PredictData)
admin.site.register(Weather)
admin.site.register(User)