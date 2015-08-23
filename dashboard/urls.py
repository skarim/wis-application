from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'dashboard.views.dashboard'),
    url(r'^settings/$', 'dashboard.views.account_settings'),

    # admin views
    url(r'^volunteers/$', 'dashboard.views.manage_volunteers'),
    url(r'^volunteers/view/', 'dashboard.views.view_volunteer'),
    url(r'^dates/$', 'dashboard.views.manage_dates'),
    url(r'^dates/view/', 'dashboard.views.view_date'),

    # volunteer views
    url(r'^register/', 'dashboard.views.volunteer_register'),
    url(r'^manage/', 'dashboard.views.volunteer_manage_registrations'),
)