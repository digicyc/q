from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from q.common import admin_keyword_search

from q.ebooks.admin import BookAdmin
from q.ebooks import models

@login_required
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

@login_required
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

@login_required
def book_info(request, template_name="ebooks/book_info.html", *args, **kwargs):
    """
    Display the information for the book
    """
    ctx = {}

    book_slug = kwargs.get('book_slug')
    book = get_object_or_404(models.Book, slug=book_slug)

    ctx.update({ 'book': book })  

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

@login_required
def book_checkout(request,  *args, **kwargs):
	
    book_key = kwargs.get('book_key')
    book = get_object_or_404(models.Book, key__exact=book_key)
    user = User.objects.get(username__exact=request.user.username)
	
    try:
        if book.checked_out.username == user.username:
	        book.checked_out = None
    except:
        book.checked_out = user
        
    book.save()
	
    return HttpResponseRedirect(reverse('book_info', kwargs={'book_slug': book.slug}))
	
