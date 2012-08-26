from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^reload_wsgi/', 'q.common.touch_wsgi'),

    url(r'^books/', include('ebooks.urls', namespace="books")),
    #url(r'^users/', include('accounts.urls')),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^api/', include('api.urls', namespace="api")),
)

urlpatterns += patterns('accounts.views',
    url(r'^$', 'login'),
    url(r'^signup/$', 'signup', name="signup"), 
    url(r'^login/$',  'login', name='login'),
    url(r'^logout/$',  'logout', name='logout'),
    url(r'^invited/(?P<invitation_key>[\w\d\-]+)/$', 'invited', name='invitation_invited'),
)


urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
)
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)

if settings.DEFAULT_FILE_STORAGE == "django.core.files.storage.FileSystemStorage":

    urlpatterns += patterns('django.views.static',
        (r'books/covers/(?P<path>.*)$', 'serve',
             {'document_root': os.path.join(settings.MEDIA_ROOT,'books','covers')}),
        (r'books/files/(?P<path>.*)$', 'serve',
             {'document_root': os.path.join(settings.MEDIA_ROOT,'books','files')}),
)


#view user profiles.
#urlpatterns += patterns('',
#    url(r'(?P<username>[\w\d\-]+)$', view_user, name="view_user"),
#)