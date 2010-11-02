from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from q.common import admin_keyword_search

from q.ebooks.admin import BookAdmin
from q.ebooks import models
from q.ebooks import forms 

@login_required
def index(request, template_name="ebooks/index.html"):
    ctx = {}
    books = None

    if request.GET.has_key('q') and request.GET['q'].strip() != "":
        template_name = "ebooks/search.html"
        books = admin_keyword_search(models.Book,
                BookAdmin.search_fields, request.GET['q'])

    else:
        books = models.Book.objects.order_by("-create_time")[:15].distinct()

    ctx.update({ 'books': books })
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
def books_by_type(request, template_name="ebooks/search.html",  *args, **kwargs):
    ctx = {}

    filter_type = kwargs.get('type').lower()

    if filter_type == "author":
        letter = kwargs.get('letter')
        books = models.Book.objects.filter(authors__lastname__istartswith=letter).distinct().order_by('authors__lastname', 'authors__firstname')
    elif filter_type == "title":
        letter = kwargs.get('letter')
        books = models.Book.objects.exclude(title__iregex=r'^(an?|the)+').filter(title__istartswith=letter).distinct().order_by('title', 'authors__lastname', 'authors__firstname')

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
    checkouts = models.CheckOut.objects.filter(book=book)
    ctx.update({ 'book': book, 'checkouts':checkouts })

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
    ctx = {}
    
    book_key = kwargs.get('book_key')
    book = get_object_or_404(models.Book, key__exact=book_key)
    user = User.objects.get(username__exact=request.user.username)
    owners = book.owners.all()
    
    # is this a checkin??
    try:
        if book.checked_out.username == user.username:
            book.checked_out = None
            book.save()
            
            book_owner_id = owners[0].user.pk
            ownership = models.Ownership.objects.get(user__pk=book_owner_id, book=book)
            ownership.checked_out = None
            ownership.save()
            
            return HttpResponseRedirect(reverse('book_info', kwargs={'book_slug': book.slug}))
    except:
        pass
        
    # or is it a checkout?  
    if len(owners) > 1:
        if request.method == "POST":
            # owner has been selected.
            checkout_form = forms.CheckOutFromUser(request.POST, owners=owners) 
            if checkout_form.is_valid():
 
                book_owner_id = checkout_form.cleaned_data["owners"]
                print book_owner_id
            
        else:
            checkout_form = forms.CheckOutFromUser(owners=owners)
            ctx.update({ 'book': book, 'checkout_form':checkout_form })
            template_name = "ebooks/checkout_from_user.html"
            return render_to_response(template_name, RequestContext(request, ctx))
    else:
        book_owner_id = owners[0].user.pk
    
    book_owner = User.objects.get(pk__exact=book_owner_id)
    #update Ownership to reflect Checkout.
    ownership = models.Ownership.objects.get(user=book_owner, book=book)
    ownership.checked_out = user
    ownership.save()
    
    #update book to reflect Checkout Status
    checkout = models.CheckOut()
    checkout.user = user
    checkout.book = book
    checkout.save()
    
    book.checked_out = user
    book.save()

    return HttpResponseRedirect(reverse('book_info', kwargs={'book_slug': book.slug}))
