from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display, name='diary'), # display.html
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='diary_detail'), # detail.html
    url(r'^new/$', views.new, name='diary_new'), # newdiary.html
    url(r'^edit/(?P<pk>\d+)/$', views.edit, name='diary_edit'), # edit.html
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='diary_delete'),

    url(r'^map/$', views.map, name='map'), # display-map.html
    url(r'^tag/$', views.tag, name='tag'), # display-tag.html

    url(r'^search/$', views.search, name='diary_search'), # search.html
    url(r'^search/results/$', views.search_result, name='diary_search_result'), # search.html
]
