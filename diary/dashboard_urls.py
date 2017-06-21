from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^new/$', views.new, name='diary_new'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit, name='diary_edit'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='diary_delete'),
]
