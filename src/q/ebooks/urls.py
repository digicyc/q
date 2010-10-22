from django.conf.urls.defaults import *

urlpatterns = patterns('q.ebooks.views',
    (r'^$', 'index'),
    (r'^latest_books.rss$', 'latest_books_rss'),
    (r'^book/(?P<book_slug>[\w\d\-]+)/$', 'book_info'),
    (r'^(?P<type>(author|title))/$', 'books_by_type'),
    (r'^(?P<type>(author|title))/(?P<letter>[\w]+)/$', 'books_by_type'),
)
