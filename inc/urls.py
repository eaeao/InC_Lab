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
from inc.epl import views as eplview
from inc.erroranalysis import views as erroranalysisview
from inc.evaluation import views as evaluationview
from inc.itembank import views as itembankview
from inc.main import views as mainview

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', mainview.main),
    url(r'^account/$', mainview.account),
    url(r'^account/password/$', mainview.account_password),
    url(r'^auth/login/$', mainview.auth_login),
    url(r'^auth/logout/$', mainview.auth_logout),
    url(r'^auth/register/$', mainview.auth_register),
    url(r'^auth/register/school/$', mainview.auth_register_school),
    url(r'^paper/$', mainview.paper),
    url(r'^paper/add/$', mainview.paper_add),
    url(r'^book/$', mainview.book),
    url(r'^itembank/$', itembankview.itembank_testpaper),
    url(r'^itembank/question/$', itembankview.itembank_question),
    url(r'^itembank/question/mine/', itembankview.itembank_question_mine),
    url(r'^itembank/question/other/', itembankview.itembank_question_other),
    url(r'^itembank/question/detail/(?P<qid>\d+)$', itembankview.itembank_question_detail),
    url(r'^itembank/question/write/$', itembankview.itembank_question_write),
    url(r'^itembank/question/write/selects/$', itembankview.itembank_write_selects),
    url(r'^itembank/question/delete/(?P<qid>\d+)$', itembankview.itembank_delete),
    url(r'^itembank/testpaper/$', itembankview.itembank_testpaper),
    url(r'^itembank/testpaper/mine/', itembankview.itembank_testpaper_mine),
    url(r'^itembank/testpaper/other/', itembankview.itembank_testpaper_other),
    url(r'^itembank/testpaper/write/$', itembankview.itembank_testpaper_write),
    url(r'^itembank/testpaper/detail/(?P<tpid>\d+)$', itembankview.itembank_testpaper_detail),
    url(r'^menu/(?P<menu_id>\d+)$', mainview.menu),
    url(r'^menu/edit/(?P<menu_id>\d+)$', mainview.page_edit),
    url(r'^page/upload/$', mainview.page_upload),
    url(r'^board/reply/delete/$', mainview.board_reply_delete),
    url(r'^board/reply/post/$', mainview.board_reply_post),
    url(r'^board/reply/(?P<board_id>.*)$', mainview.board_reply),
    url(r'^board/delete/$', mainview.board_delete),
    url(r'^board/write/(?P<menu_id>.*)$', mainview.board_write),
    url(r'^board/detail/(?P<board_id>.*)$', mainview.board_detail),
    url(r'^board/modify/(?P<board_id>.*)$', mainview.board_modify),
    url(r'^erroranalysis/$', erroranalysisview.erroranalysis),
    url(r'^erroranalysis/(?P<qid>\d+)$', erroranalysisview.erroranalysis),
    url(r'^erroranalysis/result/$', erroranalysisview.erroranalysis_result),
    url(r'^erroranalysis/analysis/(?P<qid>\d+)$', erroranalysisview.erroranalysis_analysis),
    url(r'^erroranalysis/analysis/result/$', erroranalysisview.erroranalysis_analysis_result),
    url(r'^evaluation/$', evaluationview.evaluation),
    url(r'^evaluation/result/(?P<qid>\d+)$', evaluationview.evaluation_result),
    url(r'^evaluation/detail/(?P<qid>\d+)$', evaluationview.evaluation_detail),
    url(r'^evaluation/write/$', evaluationview.evaluation_write),
    url(r'^epl/(?P<eplname>[\w\-]+)/$', eplview.epl),
    url(r'^test/$', mainview.test),
    url(r'^JudgeOnline/$', mainview.JudgeOnline),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]