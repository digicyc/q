import operator
from django.db.models import Q
from django.db.models.query import QuerySet


def admin_keyword_search(model, fields, keywords):
    """
    """

    if not keywords:
        return []

    keywords = keywords.split(" ")
    qs = QuerySet(model)
    for keyword in keywords:
        or_queries = [ Q(**{'%s__icontains' % field: keyword}) for field in fields ]
        other_qs = QuerySet(model)
        if qs.select_related:
            other_qs = other_qs.select_related()
        other_qs = other_qs.filter(reduce(operator.or_, or_queries))
        qs = qs & other_qs

    return qs

def cache_book_info(book_id, gid=None):
    from urllib2 import urlopen

    from gdata.books import Book as GBook

    from q.ebooks.models import Book, Author

    book = Book.objects.get(id=book_id)

    if gid is None:
        gid = book.gid

    if gid is None:
        return -1

    volume_xml = urlopen("http://www.google.com/books/feeds/volumes/%s" % gid).read()
    gbook = GBook.FromString(volume_xml)

    book.title = gbook.title.text
    book.metarating = gbook.rating.average
    book.description = gbook.description.text
    book.published_year = gbook.date.text

    for gauthor in gbook.creator:
        try:
            author = Author.objects.get(lastname=gauthor.text.split(" ")[-1])
        except Author.DoesNotExist, e:
            author = Author()
            author.firstname = " ".join(gauthor.text.split(" ")[:-1])
            author.lastname = gauthor.text.split(" ")[-1]
            author.save()


        book.authors.add(author)

    for identifier in gbook.identifier:
        id = identifier.text
        if id.startswith("ISBN:"):
            isbn = id.replace("ISBN:", "")
            if len(isbn) == 13:
                book.isbn13 = isbn
            elif len(isbn) == 10:
                book.isbn10 = isbn
        else:
            book.gid = id

    book.save()

