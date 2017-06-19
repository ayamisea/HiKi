from django.conf.urls import url
from django.contrib.auth import views as auth

from . import views


urlpatterns = [
    url(r'^signup/$', views.user_signup, name='signup'),
    url(r'^verify/(?P<verification_key>[-:\w]+)/$',
        views.user_verify, name='user_verify'),
    url(r'^verification_request',
        views.request_verification, name='request_verification'),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', auth.logout, {'next_page': '/accounts/'}, name='logout'),
    url(r'^profile/$', views.user_profile_update, name='user_profile_update'),

    url(r'^password-change/$', views.password_change, name='password_change'),

    url(r'^$', views.accounts, name='accounts'),
]
