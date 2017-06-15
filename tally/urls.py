from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display,name='tally_display'), # display.html
    url(r'^new$', views.newTally,name='tally_new'), 
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='tally_detail'), # detail.html
    url(r'^edit/(?P<pk>\d+)/$', views.editTally, name='tally_edit'),
    url(r'^summary$', views.summary, name='tally_summary'),
]