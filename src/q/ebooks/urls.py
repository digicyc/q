from django.conf.urls.defaults import *

from djangoratings.views import AddRatingFromModel

from q.ebooks.api import email_kindle, change_book_attribute, update_tag, get_tags, i_own_this_book

urlpatterns = patterns('q.ebooks.views',
    url(r'^$', 'index', name="index"),
    url(r'^latest_books.rss$', 'latest_books_rss', name="latest_books_rss"),

    url(r'^add/$', 'add_book', name="add_book"),
    url(r'^add/(?P<isbn>\d+)/$', 'add_book', name="isbn_search"),

    url(r'^checkout/(?P<book_key>[\w\d\-]+)/$', 'book_checkout', name="book_checkout"),
    url(r'^tags/(?P<tag>[\ \w\d\-]+)/$', 'view_tag', name="view_tag"),

    url(r'^download/(?P<download_key>[\w\d\=]+)/$', 'download_format', name="download_format"),

    url(r'^series/(?P<series_slug>[\w\d\-]+)/$', 'books_by_series', name="books_by_series"),

    url(r'^api/email_kindle/(?P<book_id>\d+)/$', email_kindle, name="email_kindle"),
    url(r'^api/change_attribute/(?P<book_id>\d+)/$', change_book_attribute, name="change_book_attribute"),
    url(r'^api/update_tag/$', update_tag, name="update_tag"),
    url(r'^api/get_tags/$', get_tags, name="get_tags"),
    url(r'^api/i_own_this_book/$', i_own_this_book, name="i_own_this_book"),
    url(r'^api/rate/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'ebooks',
        'model': 'book',
        'field_name': 'rating',
    }),

    url(r'^(?P<book_slug>[\w\d\-]+)/$', 'book_info', name="book_info"),
    url(r'^(?P<type>(author|title))/$', 'books_by_type', name="books_by_type"),
    url(r'^(?P<type>(author|title))/(?P<letter>[\w]+)/$', 'books_by_type', name="books_by_author"),
)
