from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'dashboard.views.dashboard'),

    # admin views
    url(r'^volunteers/$', 'dashboard.views.manage_volunteers'),
    url(r'^volunteers/view/', 'dashboard.views.view_volunteer'),
    url(r'^dates/', 'dashboard.views.manage_dates'),

    # volunteer views
    # go here
)