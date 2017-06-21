"""hiki_diary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

from core.views import index, search , search_results
from diary import views as diary
from gallery import views as gallery
from users.views import user_dashboard

urlpatterns = i18n_patterns(
    url(r'^$', index, name='index'),
    url(r'^search/$', search, name='search'),
    url(r'^search/(?P<q>\w+)/$', search_results, name='search_results'),

    url(r'^accounts/', include('users.urls')),
    url(r'^diary/', include('diary.urls')),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^tally/', include('tally.urls')),

    url(r'^dashboard/$', user_dashboard, name='user_dashboard'),
    url(r'^dashboard/diary/', include('diary.dashboard_urls')),
    url(r'^dashboard/gallery/', include('gallery.dashboard_urls')),
    url(r'^dashboard/tally/', include('tally.dashboard_urls')),
)

# set-langauge and admin should not be prefixed with language.
urlpatterns += [
    url(r'^set-language/$', set_language, name='set_language'),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
