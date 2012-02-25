from gdata.books import Book, BookFeed
from urllib2 import urlopen

class GoogleBook(object):
    
    def __init__(self, isbn):
        if isbn is None and gid is None:
            raise MissingIdException("Must provide at least one: gid %s isbn %s" (gid, isbn))
        
        self.isbn = isbn
        self.google_id = None
        self.authors = []
        
        self._populate()
        
    def _populate(self):
        search_xml = urlopen("http://books.google.com/books/feeds/volumes?q=ISBN%s" % self.isbn).read()
        search_feed = BookFeed.FromString(search_xml)
        self.google_id = search_feed.entry[0].identifier[0].text
        
        volume_xml = urlopen("http://www.google.com/books/feeds/volumes/%s" % self.google_id).read()
        gbook = Book.FromString(volume_xml)
        print gbook.creator
        for gauthor in gbook.creator:
            gauthor = gauthor.text
            self.authors.append(gauthor)
            
class MissingIdException(Exception): pass

if __name__ == "__main__":
    g = GoogleBook(isbn="9780142000274")
    print g.authors