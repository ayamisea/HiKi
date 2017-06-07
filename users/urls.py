from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^signup/$', views.user_signup),
    url(r'^login/$', views.user_login),
]
