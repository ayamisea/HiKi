from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^new/', views.new, name='gallery_new'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit, name='gallery_edit'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='gallery_delete'),
    url(r'^diary-image-show/$', views.diary_image_show),
]
