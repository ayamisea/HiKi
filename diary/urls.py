from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display, name='diary'),
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='diary_detail'),
    url(r'^map/$', views.map, name='map'),
    url(r'^tag/$', views.tag, name='tag'),
]
