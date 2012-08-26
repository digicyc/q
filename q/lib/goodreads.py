from httplib import HTTPConnection
import xml.etree.cElementTree as ElementTree

from django.conf import settings

class GoodReads(object):
    authors = dict()
    title = ""

    def __init__(self, isbn=None):
        self.http = HTTPConnection("www.goodreads.com")

        if isbn is not None:
            self.isbn = isbn
            self._populate(isbn)

    def _build_dict(self, passed_elem, parent=None):

        passed_elem_children = passed_elem.getchildren()
        if len(passed_elem_children) == 0 or "isbn" in passed_elem.tag:
            text = None

            if passed_elem.text is not None:
                text = passed_elem.text.strip()

            if parent is not None:
                parent[passed_elem.tag] = text
            else:
                self.__dict__[passed_elem.tag] = text

        else:
            if parent is not None:
                parent[passed_elem.tag] = dict()
                p = parent[passed_elem.tag]
            else:
                self.__dict__[passed_elem.tag] = dict()
                p = self.__dict__[passed_elem.tag]
            for child in passed_elem_children:
                self._build_dict(child, p)


    def _populate(self, isbn):
        url = "/book/isbn?isbn=%s&key=%s" %(isbn, settings.GOODREADS_KEY)
        self.http.request('GET', url)
        response = self.http.getresponse()

        et = ElementTree.parse(response)
        etbook = et.find("book")
        for child in etbook.getchildren():
            self._build_dict(child)
        del self.http

class InvalidJSONResponseError(Exception): pass
class ISBNNotFoundError(Exception): pass
class ServerThrewError(Exception): pass

if __name__ == "__main__":
    gr = GoodReads("9780141185125")