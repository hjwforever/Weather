from django.contrib import admin
from . import models
from app.models import *
# Register your models here.


# admin.site.register(models.User)
class PredictDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'tmin', 'tmax', 'tavg', 'prcp')


class HistoryDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'tmin', 'tmax', 'tavg', 'prcp')


admin.site.register(User)
admin.site.register(ConfirmString)
admin.site.register(HistoryData, HistoryDateAdmin)
admin.site.register(PredictData, PredictDataAdmin)
admin.site.register(Weather)
admin.site.register(Memorandum)

