from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'dashboard.views.dashboard'),

    # admin views
    url(r'^volunteers/', 'dashboard.views.manage_volunteers'),

    # volunteer views
    # go here
)