from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^regist/$', views.regist, name = 'regist'),
    url(r'^index/$', views.index, name = 'index'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^list', views.course_list, name='course_list'),
    url(r'^course/(?P<pk>[0-9]+)/$', views.course_detail, name='course_detail'),
    url(r'^course/new/$', views.course_new, name='course_new'),
    url(r'^course/(?P<pk>\d+)/comment/$', views.comment_new, name='comment_new'),
    url(r'^course/rating/(?P<pk>\d+)/(?P<profid>\d+)/$', views.rating, name='rating'),
]
