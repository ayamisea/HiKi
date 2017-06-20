from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display, name='gallery'), # display-media.html
    url(r'^new/', views.new, name='gallery_new'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit, name='gallery_edit'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='gallery_delete'),
    url(r'^media-upload/$', views.media_upload), # upload-media.html
    url(r'^media-upload-show/$', views.media_upload_show), # upload-media-display.html
]
