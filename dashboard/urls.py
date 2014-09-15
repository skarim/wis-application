from django.conf.urls import patterns, url
from django.shortcuts import redirect


urlpatterns = patterns(
    '',
    url(r'^$', 'dashboard.views.dashboard'),
)