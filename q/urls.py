from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from accounts.views import login, logout, invited, signup, view_user

admin.autodiscover()

urlpatterns = patterns('',
    (r'^reload_wsgi/', 'q.common.touch_wsgi'),

    (r'^books/', include('ebooks.urls')),
    #(r'^users/', include('accounts.urls')),
    (r'^accounts/', include('accounts.urls')),                  
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^$', login),
    url(r'^signup$', signup, name="signup"), 
    url(r'^login/$',  login, name='login'),
    url(r'^logout/$',  logout, name='logout'),
    url(r'^invited/(?P<invitation_key>[\w\d\-]+)$', invited, name='invitation_invited'),
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