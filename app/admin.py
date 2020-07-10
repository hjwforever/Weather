from django.contrib import admin
from . import models
from app.models import *
# Register your models here.


# admin.site.register(models.User)
class PredictDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'tmin', 'tmax', 'tavg','weather')
    search_fields = ('date', 'tmin', 'tmax', 'tavg','weather')
    date_hierarchy = 'date'


class HistoryDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'tmin', 'tmax', 'tavg','weather')
    search_fields = ('date', 'tmin', 'tmax', 'tavg', 'weather')
    date_hierarchy = 'date'


admin.site.register(User)
admin.site.register(ConfirmString)
admin.site.register(HistoryData, HistoryDateAdmin)
admin.site.register(PredictData, PredictDataAdmin)
# admin.site.register(Weather)
admin.site.register(Memorandum)

admin.site.site_header = 'Six-Single-Dogs天气预测后台管理系统'
admin.site.site_title = 'Six-Single-Dogs'
