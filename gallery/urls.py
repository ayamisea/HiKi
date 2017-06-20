from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^map/$', views.map,name='diary_map'), # display-map.html
    url(r'^media/$', views.media,name='diary_media'), # display-media.html
    url(r'^media-upload/$', views.media_upload), # upload-media.html
    url(r'^media-upload-show/$', views.media_upload_show), # upload-media-display.html
]
