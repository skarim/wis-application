from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'application.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'dashboard/', include('dashboard.urls')),

    # fallback to auth
    url(r'', include('authorization.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
