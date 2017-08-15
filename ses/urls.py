
from django.conf.urls import url
from . import views
from . import admin

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^editSeat/$', views.editSeat),
    url(r'^searchSeat/$', views.index),
    url(r'^changeSeat/$', views.changeSeat),
    url(r'^editScore/$', views.editScore),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^subjectManage/$', views.subjectManage),
    url(r'^scoreListQuery/$', views.scoreListQuery),
    url(r'^giveScoreRule/$', views.giveScoreRule),
    url(r'^addScoreRule/$', views.addScoreRule),
    url(r'^getScoreRules/$', views.getScoreRules),
    url(r'^getNotClaSubByScoreRule/$', views.getNotClaSubByScoreRule),
    url(r'^deleteScore/$', views.deleteScore),
    url(r'^sortSeat/$', views.sortSeat),
    url(r'^outputScoreListByExcel/$', views.outputScoreListByExcel),
    url(r'^addClassroom/$', views.addClassroom),
    url(r'^getNotClaBySubGra/$', views.getNotClaBySubGra),
]
