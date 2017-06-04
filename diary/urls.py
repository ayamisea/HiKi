from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^unit_test/$', views.unit_test), # unit_test.html
    url(r'^display/$', views.display), # display.html
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='detail'), # detail.html
    url(r'^map/$', views.map), # display-map.html
    url(r'^media/$', views.media), # display-media.html
    url(r'^tag/$', views.tag), # display-tag.html
    url(r'^new/$', views.newdiary), # newdiary.html
    url(r'^media-upload/$', views.media_upload), # upload-media.html
    url(r'^media-upload-show/$', views.media_upload_show), # upload-media-display.html
    url(r'^test/$', views.test),# test.html  #ignore it
]
