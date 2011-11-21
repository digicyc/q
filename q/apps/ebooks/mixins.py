from httplib import HTTPConnection

from django.conf import settings

class GoodReadsBookMixin(object):
    def __init__(self):
        self.http = HTTPConnection("www.goodreads.com")

    def get_goodreads_id(self):
        url = "/book/isbn_to_id/%s?key=%s" % (self.isbn13, settings.GOODREADS_KEY)
        self.http.request('GET', url)
        return self.http.getresponse().read()