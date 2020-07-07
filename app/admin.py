from django.contrib import admin
from . import models
from app.models import *
# Register your models here.


# admin.site.register(models.User)
admin.site.register(User)
admin.site.register(ConfirmString)
admin.site.register(HistoryData)
admin.site.register(PredictData)
admin.site.register(Weather)

