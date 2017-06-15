from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display), # display.html
    url(r'^new$', views.newTally), 
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='detail'), # detail.html
    url(r'^edit/(?P<pk>\d+)/$', views.editTally),
    url(r'^summary$', views.summary),
]