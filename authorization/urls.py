from django.conf.urls import patterns, url
from django.shortcuts import redirect


urlpatterns = patterns(
    '',
    url(r'^signup/', 'authorization.views.create_account'),
    url(r'^login/', 'authorization.views.sign_in'),
    url(r'^logout/', 'authorization.views.logout_user'),

    # redirect everything else to login
    url(r'', lambda x: redirect('/login/')),
)