from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from q.accounts.views import login, logout


admin.autodiscover()

urlpatterns = patterns('',
    (r'^books/', include('q.ebooks.urls')),
    (r'^users/', include('q.accounts.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', login),
    url(r'^login/$',  login, name='login'),
    url(r'^logout/$',  logout, name='logout'),
    (r'^comments/', include('django.contrib.comments.urls')),
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
