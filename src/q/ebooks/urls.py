from django.conf.urls.defaults import *
from q.ebooks.views import index, book_info, view_tag, latest_books_rss, books_by_type, isbn_search, book_checkout, download_format
from q.ebooks.api import email_kindle, change_book_attribute, update_tag, get_tags

urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^latest_books.rss$', latest_books_rss, name="latest_books_rss"),
    url(r'^(?P<book_slug>[\w\d\-]+)/$', book_info, name="book_info"),
    url(r'^(?P<type>(author|title))/$', books_by_type, name="books_by_type"),
    url(r'^(?P<type>(author|title))/(?P<letter>[\w]+)/$', books_by_type, name="books_by_author"),
    url(r'^add/(?P<isbn>\d+)/$', isbn_search, name="isbn_search"),
    url(r'^checkout/(?P<book_key>[\w\d\-]+)/$', book_checkout, name="book_checkout"),
    url(r'^tags/(?P<tag>[\w\d\-]+)/$', view_tag, name="view_tag"),
    url(r'^download/(?P<download_key>[\w\d\=]+)/$', download_format, name="download_format"),
    
    
    url(r'^api/email_kindle/(?P<book_id>\d+)/$', email_kindle, name="email_kindle"),
    url(r'^api/change_attribute/(?P<book_id>\d+)/$', change_book_attribute, name="change_book_attribute"),
    url(r'^api/update_tag/$', update_tag, name="update_tag"),
    url(r'^api/get_tags/$', get_tags, name="get_tags"),
)
