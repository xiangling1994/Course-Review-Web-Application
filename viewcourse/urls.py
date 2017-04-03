from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.course_list, name= 'course_list'),
    url(r'^collection/$', views.collection, name= 'collection'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^regist/$', views.regist, name = 'regist'),
    url(r'^index/$', views.index, name = 'index'),
    url(r'^change_password', views.change_password, name= 'change_password'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^list', views.course_list, name= 'course_list'),
    url(r'^course/(?P<pk>[0-9]+)/$', views.course_detail, name= 'course_detail'),
    url(r'^course/new/$', views.course_new, name= 'course_new'),
    url(r'^course/(?P<pk>\d+)/comment/$', views.comment_new, name= 'comment_new'),
    url(r'^course/agree(?P<pk>\d+)/(?P<cid>\d+)/$', views.agree, name = 'agree'),
    url(r'^course/disagree(?P<pk>\d+)/(?P<cid>\d+)/$', views.disagree, name = 'disagree'),
    url(r'^course/rating/(?P<pk>\d+)/(?P<profid>\d+)/$', views.rating, name= 'rating'),
]
