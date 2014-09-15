from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # dashboard
    url(r'dashboard/', include('dashboard.urls')),

    # fallback to auth
    url(r'', include('authorization.urls')),
)
