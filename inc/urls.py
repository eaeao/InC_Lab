"""inc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from inc import settings
from inc.itembank import views as itembankview
from inc.main import views as mainview

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', mainview.main),
    url(r'^auth/login/$', mainview.auth_login),
    url(r'^auth/logout/$', mainview.auth_logout),
    url(r'^auth/register/$', mainview.auth_register),
    url(r'^itembank/$', itembankview.itembank),
    url(r'^itembank/detail/(?P<qid>\d+)$', itembankview.itembank_detail),
    url(r'^itembank/write/$', itembankview.itembank_write),
    url(r'^itembank/write/selects/$', itembankview.itembank_write_selects),
    url(r'^itembank/delete/(?P<qid>\d+)$', itembankview.itembank_delete),
    url(r'^JudgeOnline/$', mainview.JudgeOnline),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]