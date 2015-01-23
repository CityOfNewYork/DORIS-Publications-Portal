from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('gpp.urls')),  # ADD THIS NEW TUPLE!
#     url(r'^admin/', include(admin.site.urls)),  # ADD THIS LINE
)