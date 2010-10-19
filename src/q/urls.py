from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^books/', include('q.ebooks.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('django.views.static',
	    (r'^css/(?P<path>.*)$', 'serve',
	        {'document_root': settings.TEMPLATE_DIRS[0]+'/css/'}),
	    (r'^images/(?P<path>.*)$', 'serve',
	        {'document_root': settings.TEMPLATE_DIRS[0]+'/images/'}),
	    (r'^javascript/(?P<path>.*)$', 'serve',
	        {'document_root': settings.TEMPLATE_DIRS[0]+'/javascript/'}),
	)