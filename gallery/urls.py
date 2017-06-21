from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.display, name='gallery'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit, name='image_edit'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='image_delete'),
]
