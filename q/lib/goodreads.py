from httplib import HTTPConnection

from q import settings
import json

import xml.etree.cElementTree as ElementTree


class GoodReads(object):
    def __init__(self, isbn=None):
        self.http = HTTPConnection("www.goodreads.com")
        self.stats = None

        if isbn is not None:
            self._populate(isbn)

    def _populate(self, isbn):
        url = "/book/isbn?isbn=%s&key=%s" %(isbn, settings.GOODREADS_KEY)
        self.http.request('GET', url)
        response = self.http.getresponse()
        for event, elem in ElementTree.iterparse(response):
            if event == "end" and elem.tag == "book":
                for elem in elem.iter():
                    if elem.tag == "book_link" or elem.tag == "shelf" or elem.tag == "reviews_widget": continue
                    if len(elem.getchildren()) > 0:
                        parent_elem = elem.tag
                        self.__dict__[elem.tag] = dict()
                        for elem2 in elem.iter():
                            if len(elem2.getchildren()) > 0:
                                parent_elem2 = elem.tag
                                self.__dict__[elem2.tag] = dict()
                                for elem3 in elem2.getchildren():

                                    self.__dict__[parent_elem2][elem3.tag] = elem3.text
                            else:
                                self.__dict__[parent_elem][elem2.tag] = elem2.text
                    else:
                        self.__dict__[elem.tag] = elem.text

class InvalidJSONResponseError(Exception): pass
class ISBNNotFoundError(Exception): pass

if __name__ == "__main__":
    gr = GoodReads()

    print gr.get_book_info("0441172717")