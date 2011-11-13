from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from decomposition.views import dashboard, gen, create, assign
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       ('^$', dashboard ),
                       ('^login/$', login ),
                       ('^logout/$', logout ),
                       ('^create/$', create ),
                       (r'^assignment/(\w+)/?', assign ),
                       ('^gen/$', gen ),

    # Examples:
    # url(r'^$', 'decomposition.views.home', name='home'),
    # url(r'^decomposition/', include('decomposition.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
