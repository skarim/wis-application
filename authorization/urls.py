from django.conf.urls import patterns, url
from django.shortcuts import redirect


urlpatterns = patterns(
    '',
    url(r'^activate/', 'authorization.views.create_account'),
    url(r'^login/', 'authorization.views.sign_in'),
    url(r'^forgot/', 'authorization.views.forgot_password'),
    url(r'^logout/', 'authorization.views.logout_user'),

    # redirect everything else to login
    url(r'', lambda _: redirect('/login/')),
)