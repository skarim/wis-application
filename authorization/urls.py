from django.conf.urls import patterns, url
from django.shortcuts import redirect


urlpatterns = patterns(
    '',
    url(r'^logout/', 'authorization.views.logout_user'),
    url(r'^login/', 'authorization.views.sign_in'),

    # redirect everything else to login
    url(r'', lambda x: redirect('/login/')),
)