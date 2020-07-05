from django.urls import path
from app import views
from django.urls import include

urlpatterns = [
    # path('', views.html, name='html'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('index/', views.IndexView.as_view(), name='demo'),
    path('login/', views.login, name='login'),
    # path('show/', views.show_data, name='show_data'),
    path('upload/', views.upload_file, name='upload_file'),
    path('show/', views.get_test, name='get_test'),
    path('history/', views.history_page, name='history'),
    path('transfer/', views.transfer_history, name='transfer_data'),
    path('html/', views.login),
    path('register/', views.register,name='register'),
    path('logout/', views.logout),
    path('captcha/', include('captcha.urls')),
    path('confirm/', views.user_confirm),
    path('line/', views.ChartView.as_view(), name='line'),
    path('bar/', views.ChartView.as_view(), name='bar'),
    path('newhome/', views.home_index),
    path('BJ/', views.beijingweather),
    path('hjhTest/', views.hjh_test),

]

# from django.conf.urls import include, url
# from django.contrib import admin
# from app import views as app_views
#
# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^$', app_views.home, name='home'),
# ]