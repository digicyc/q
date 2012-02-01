from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

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

if settings.DEBUG:
    import os.path
    urlpatterns += patterns('django.views.static',
        (r'^css/(?P<path>.*)$', 'serve',
            {'document_root': os.path.join(settings.MEDIA_ROOT,'css')}),
        (r'^images/(?P<path>.*)$', 'serve',
             {'document_root': os.path.join(settings.MEDIA_ROOT,'images')}),
        (r'^javascript/(?P<path>.*)$', 'serve',
             {'document_root': os.path.join(settings.MEDIA_ROOT,'javascript')}),
        (r'^font/(?P<path>.*)$', 'serve',
             {'document_root': os.path.join(settings.MEDIA_ROOT,'font')}),
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