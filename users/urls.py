from django.conf.urls import url
from django.contrib.auth import views as auth

from . import views


urlpatterns = [
    url(r'^signup/$', views.user_signup, name='signup'),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', auth.logout, {'next_page': '/accounts/'}, name='logout'),

    url(r'^$', views.home,name='account'),
]
