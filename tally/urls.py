from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display, name='tally'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='tally_delete'),
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='tally_detail'),
    url(r'^edit/(?P<pk>\d+)/$', views.editTally, name='tally_edit'),
    url(r'^new$', views.new, name='tally_new'),
    url(r'^summary$', views.summary, name='tally_summary'),
]
