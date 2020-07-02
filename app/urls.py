from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
]

# from django.conf.urls import include, url
# from django.contrib import admin
# from app import views as app_views
#
# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^$', app_views.home, name='home'),
# ]