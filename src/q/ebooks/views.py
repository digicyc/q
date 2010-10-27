from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from q.common import admin_keyword_search

from q.ebooks.admin import BookAdmin
from q.ebooks import models

#@login_required
def index(request, template_name="ebooks/index.html"):
    ctx = {}
    books = None
    
    if request.GET.has_key('q') and request.GET['q'].strip() != "":
        template_name = "ebooks/search.html"
        books = admin_keyword_search(models.Book,
                BookAdmin.search_fields, request.GET['q'])  
        
    else:
        books = models.Book.objects.order_by("-create_time")[:15]
    
    ctx.update({ 'books': books })    
    return render_to_response(template_name, RequestContext(request, ctx))
    
def books_by_type(request, template_name="ebooks/index.html",  *args, **kwargs):
    ctx = {}
    
    filter_type = kwargs.get('type').lower()
    
    if filter_type == "author":
        letter = kwargs.get('letter')
        books = models.Book.objects.filter(authors__lastname__istartswith=letter)
    elif filter_type == "title":
        letter = kwargs.get('letter')
        books = models.Book.objects.filter(title__istartswith=letter)
    
    ctx.update({ 'books': books })  
    return render_to_response(template_name, RequestContext(request, ctx))


def latest_books_rss(request, template_name="ebooks/latest_books.rss"):
    """
    Return an RSS feed with the latest 10 books uploaded
    """
    ctx = {}
    books = models.Book.objects.all().order_by("-create_time")[:10]

    ctx.update({ 'books': books })  
    return render_to_response(template_name, RequestContext(request, ctx))

def book_info(request, template_name="ebooks/index.html", *args, **kwargs):
    """
    Display the information for the book
    """
    ctx = {}
    book = get_object_or_404(models.Book, slug=book_slug)
    
    ctx.update({ 'books': books })  
    return render_to_response(template_name, RequestContext(request, ctx))

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