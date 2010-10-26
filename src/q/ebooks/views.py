from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from q.common import admin_keyword_search

from q.ebooks.admin import BookAdmin
from q.ebooks import models

#@login_required
def index(request):
    """
    Search for a book
    """
    books = None
    if request.GET.has_key('q') and request.GET['q'].strip() != "":
        books = admin_keyword_search(models.Book,
                BookAdmin.search_fields, request.GET['q'])
        return render_to_response("ebooks/search.html",
            {
                'books': books,
            },
            context_instance=RequestContext(request)
        )

    return render_to_response("ebooks/index.html",
        {
            'books': books,
        },
        context_instance=RequestContext(request)
    )

def books_by_type(request, type, letter="a"):
    """
    Browse books by author
    """
    if type.lower() == "author":
        books = models.Book.objects.filter(authors__lastname__istartswith=letter)
    elif type.lower() == "title":
        books  = models.Book.objects.filter(title__istartswith=letter)

    return render_to_response("ebooks/index.html",
        {
            'books': books,
        },
        context_instance=RequestContext(request)
    )

def latest_books_rss(request):
    """
    Return an RSS feed with the latest 10 books uploaded
    """
    books = models.Book.objects.all().order_by("-create_time")[:10]

    return render_to_response("ebooks/latest_books.rss",
        {
            'books': books,
        },
        context_instance=RequestContext(request)
    )

def book_info(request, book_slug):
    """
    Display the information for the book
    """
    book = get_object_or_404(models.Book, slug=book_slug)

    return render_to_response("ebooks/book_info.html",
        {
            'book': book,
        },
        context_instance=RequestContext(request))

def isbn_search(isbn):
    """
    Search places for the ISBN
    """
    from gdata.books import Book, BookFeed
    from urllib2 import urlopen

    search_xml = urlopen("http://books.google.com/books/feeds/volumes?q=ISBN%s" % isbn).read()
    search_feed = BookFeed.FromString(xml)
    google_id = feed.entry[0].identifier[0].text

    volume_xml = urlopen("http://www.google.com/books/feeds/volumes/%s" % google_id).read()
    book_feed = Book.FromString(volume_xml)




