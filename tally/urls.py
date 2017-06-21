from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display, name='tally'),
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='tally_detail'),
    url(r'^summary$', views.summary, name='tally_summary'),
]
