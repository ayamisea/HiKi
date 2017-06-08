from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display), # display.html
    url(r'^new$', views.newAccount), 
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='detail'), # detail.html
]