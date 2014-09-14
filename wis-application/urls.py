from django.conf.urls import patterns, include, url

# Django Admin
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wis-application.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # fallback to auth
    url(r'', include('authorization.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
