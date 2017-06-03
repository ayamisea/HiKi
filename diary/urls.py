from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^unit_test/$', views.unit_test),
    url(r'^display/$', views.display),
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^map/$', views.map),
    url(r'^media/$', views.media),
    url(r'^new/$', views.newdiary),
    url(r'^media-upload/$', views.media_upload),
    url(r'^media-upload-show/$', views.media_upload_show),
    url(r'^test/$', views.test),
]
