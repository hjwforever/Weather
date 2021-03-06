"""Weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from app import views as app_view
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('index/', include('app.urls')),
    path('', app_view.index, name='index'),
    # path('app/', app_view.html, name='html'),
    # path('app/home/', app_view.home, name='home'),
    # path('home', app_view.home, name='home'),
    # path('index', app_view.index, name='index'),
    # path('html', app_view.html, name='html'),
]
urlpatterns += static('/appfile/', appfile_root=settings.APPFILE_ROOT)

# from django.conf.urls import include, url
# from django.contrib import admin
# from app import views as app_views
#
# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^$', app_views.home, name='home'),
# ]

