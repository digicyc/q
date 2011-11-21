from httplib import HTTPConnection

from django.conf import settings
from django.utils import simplejson
class GoodReadsBookMixin(object):
    def __init__(self):
        self.http = HTTPConnection("www.goodreads.com")
        self.stats = None
        self._get_goodreads_stats()

    def _get_goodreads_stats(self):
        """
        {
            u'work_ratings_count': 4129,
            u'isbn': u'0767905385',
            u'text_reviews_count': 98,
            u'isbn13': u'9780767905381',
            u'reviews_count': 932,
            u'work_reviews_count': 6445,
            u'average_rating': u'3.83',
            u'work_text_reviews_count': 537,
            u'ratings_count': 529,
            u'id': 375789
        }
        """
        url = "/book/review_counts.json?isbns=%s&key=%s" % (self.isbn13, settings.GOODREADS_KEY)
        self.http.request('GET', url)
        json = self.http.getresponse().read()
        data = simplejson.loads(json)
        self.stats = data["books"][0]

    def get_goodreads_id(self):
        if self.stats is None: self._get_goodreads_stats()
        if self.stats.has_key("id"):
            return self.stats.get("id")
        else:
            url = "/book/isbn_to_id/%s?key=%s" % (self.isbn13, settings.GOODREADS_KEY)
            self.http.request('GET', url)
            return self.http.getresponse().read()

    def get_goodreads_rating(self):
        if self.stats is None: self._get_goodreads_stats()
        if self.stats.has_key("average_rating"):
            return self.stats.get("average_rating")
        return 0.0

    def get_goodreads_ratings_count(self):
        if self.stats is None: self._get_goodreads_stats()
        if self.stats.has_key("work_ratings_count"):
            return self.stats.get("work_ratings_count")
        return 0.0