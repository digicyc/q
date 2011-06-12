from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from accounts.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    (r'^books/', include('ebooks.urls')),
    (r'^users/', include('accounts.urls')),
                       
    (r'^admin/', include(admin.site.urls)),
    (r'^$', login),
    url(r'^login/$',  login, name='login'),
    url(r'^logout/$',  logout, name='logout'),

    (r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG:
    import os.path
    urlpatterns += patterns('django.views.static',
        (r'^css/(?P<path>.*)$', 'serve',
            {'document_root': os.path.join(settings.MEDIA_ROOT,'css')}),
        (r'^images/(?P<path>.*)$', 'serve',
             {'document_root': os.path.join(settings.MEDIA_ROOT,'images')}),
        (r'^javascript/(?P<path>.*)$', 'serve',
             {'document_root': os.path.join(settings.MEDIA_ROOT,'javascript')}),
    )
