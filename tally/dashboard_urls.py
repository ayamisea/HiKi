from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^new$', views.new, name='tally_new'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit, name='tally_edit'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='tally_delete'),
]
