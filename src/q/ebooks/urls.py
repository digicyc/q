from django.conf.urls.defaults import *
from q.ebooks.views import index, book_info, latest_books_rss, books_by_type, isbn_search

urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^latest_books.rss$', latest_books_rss, name="latest_books_rss"),
    url(r'^(?P<book_slug>[\w\d\-]+)/$', book_info, name="book_info"),
    url(r'^(?P<type>(author|title))/$', books_by_type, name="books_by_type"),
    url(r'^(?P<type>(author|title))/(?P<letter>[\w]+)/$', books_by_type, name="books_by_author"),
    url(r'^add/(?P<isbn>\d+)/$', isbn_search, name="isbn_search"),
)
