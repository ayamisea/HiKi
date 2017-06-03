from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^unit_test/$', views.unit_test),
    url(r'^display/$', views.display),
    url(r'^new/$', views.newdiary),
    url(r'^test/$', views.test),
]
