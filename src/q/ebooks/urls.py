from django.conf.urls.defaults import *

urlpatterns = patterns('q.ebooks.views',
    (r'^$', 'index'),
    (r'^(?P<type>(author|title))/$', 'books_by_type'),
    (r'^(?P<type>(author|title))/(?P<letter>[\w]+)/$', 'books_by_type'),
)
