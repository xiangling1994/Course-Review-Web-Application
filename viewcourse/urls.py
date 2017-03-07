from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.course_list, name='course_list'),
    url(r'^course/(?P<pk>[0-9]+)/$', views.course_detail, name='course_detail'),
    url(r'^course/new/$', views.course_new, name='course_new'),
    url(r'^course/(?P<pk>\d+)/comment/$', views.comment_new, name='comment_new'),
]
