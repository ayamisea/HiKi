from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display,name='diary_display'), # display.html
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='diary_detail'), # detail.html
    url(r'^map/$', views.map,name='diary_map'), # display-map.html
    url(r'^media/$', views.media,name='diary_media'), # display-media.html
    url(r'^tag/$', views.tag,name='diary_tag'), # display-tag.html
    url(r'^new/$', views.newdiary,name='diary_new'), # newdiary.html
    url(r'^media-upload/$', views.media_upload), # upload-media.html
    url(r'^media-upload-show/$', views.media_upload_show), # upload-media-display.html
    url(r'^edit/(?P<pk>\d+)/$', views.edit,name='diary_edit'), # edit.html
    url(r'^search/$', views.search,name='diary_search'), # search.html
    url(r'^search/results/$',views.search_result,name = 'diary_search_result'), # search.html
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='diary_delete'),
]
