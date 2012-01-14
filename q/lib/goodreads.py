from httplib import HTTPConnection

from q import settings
import json

import xml.etree.cElementTree as ElementTree


class GoodReads(object):
    def __init__(self):
        self.http = HTTPConnection("www.goodreads.com")
        self.stats = None

    def get_review_counts(self, isbn):
        """
        """
        url = "/book/review_counts.json?isbns=%s&key=%s" % (isbn, settings.GOODREADS_KEY)
        self.http.request('GET', url)
        json = self.http.getresponse().read()
        try:
            data = json.loads(json)
        except ValueError, e:
            raise InvalidJSONResponseError()

        return data["books"][0]

    def get_id_from_isbn(self, isbn):
        url = "/book/isbn_to_id/?isbn=%s&format=json&key=%s" % (isbn,
                                              settings.GOODREADS_KEY)
        self.http.request('GET', url)
        response = self.http.getresponse().read()
        return response

    def get_goodreads_rating(self):
        try:
            return self.stats.get("average_rating")
        except:
            return 0.0

    def get_goodreads_ratings_count(self):
        try:
            return self.stats.get("work_ratings_count")
        except:
            return 0.0

    def get_book_info(self, isbn):
        url = "/book/isbn?isbn=%s&key=%s" %(isbn, settings.GOODREADS_KEY)
        self.http.request('GET', url)
        response = self.http.getresponse()
        book_info = dict()
        for event, elem in ElementTree.iterparse(response):
            if event == "end" and elem.tag == "book":
                for elem in elem.iter():
                    if elem.tag == "book_link" or elem.tag == "shelf" or elem.tag == "reviews_widget": continue
                    if len(elem.getchildren()) > 0:
                        parent_elem = elem.tag
                        book_info[elem.tag] = dict()
                        for elem2 in elem.iter():
                            if len(elem2.getchildren()) > 0:
                                parent_elem2 = elem.tag
                                book_info[elem2.tag] = dict()
                                for elem3 in elem2.getchildren():

                                    book_info[parent_elem2][elem3.tag] = elem3.text
                            else:
                                book_info[parent_elem][elem2.tag] = elem2.text
                    else:
                        book_info[elem.tag] = elem.text


        return book_info


class InvalidJSONResponseError(Exception): pass
class ISBNNotFoundError(Exception): pass

if __name__ == "__main__":
    gr = GoodReads()

    print gr.get_book_info("0441172717")