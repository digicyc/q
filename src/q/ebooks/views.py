import os
import urllib2
from tempfile import NamedTemporaryFile
from datetime import datetime

from django.core.files import File
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.conf import settings

from tagging.models import Tag, TaggedItem

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
        books = models.Book.objects.filter(title__istartswith=letter).distinct().order_by('title', 'authors__lastname', 'authors__firstname')

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
    checkouts = models.CheckOut.objects.filter(book__book=book).order_by('-create_time')

    print book.tags
    #related_tags = Tag.objects.related_for_model([tag], Entry)

    try:
        my_ownership = models.Ownership.objects.get(book=book, user=request.user)
    except models.Ownership.DoesNotExist, e:
        my_ownership = None

    ctx.update({ 'book': book, 'checkouts':checkouts, 'my_ownership': my_ownership })

    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
def add_book(request, isbn=None, template_name="ebooks/add/index.html", *args, **kwargs):
    """
    Begins the add book wizard process
    """
    from q.ebooks.forms import BookForm
    ctx = {}

    if request.POST.has_key('title'):
        book = models.Book()
        book.title = request.POST['title']
        book.tags = request.POST['tags']
        book.isbn10 = request.POST['isbn10']
        book.isbn13 = request.POST['isbn13']
        book.gid = request.POST['gid']
        book.description = request.POST['description']

        book.save()
        for gauthor in request.POST['authors'].split(','):
            try:
                author = models.Author.objects.get(firstname=" ".join(gauthor.split(" ")[:-1]).strip(), lastname=gauthor.split(" ")[-1])
            except Author.DoesNotExist, e:
                author = models.Author()
                author.firstname = " ".join(gauthor.split(" ")[:-1]).strip()
                author.lastname = gauthor.split(" ")[-1]
                author.save()
            book.authors.add(author)

        if book.cover == "":
            cover_link = request.POST['cover_url']
            headers = {'User-Agent': settings.DEFAULT_HTTP_HEADERS}
            f = NamedTemporaryFile(delete=False)
            f.write(urllib2.urlopen(urllib2.Request(cover_link, headers=headers)).read())
            f.filename = f.name
            f.close()

            book.cover.save(
                "temp_filename.jpg",
                File(open(f.name))
            )

            os.unlink(f.name)
        book.save()

        return HttpResponseRedirect(reverse(book_info, kwargs={'book_slug': book.slug}))

    if request.POST.has_key("isbn") and isbn is None:
        isbn= request.POST['isbn']

    if isbn:
        from gdata.books import Book, BookFeed
        from urllib2 import urlopen

        search_xml = urlopen("http://books.google.com/books/feeds/volumes?q=ISBN%s" % isbn).read()
        search_feed = BookFeed.FromString(search_xml)
        google_id = search_feed.entry[0].identifier[0].text

        #volume_xml = urlopen("http://www.google.com/books/feeds/volumes/%s" % google_id).read()
        #book_feed = Book.FromString(volume_xml)

        #cover_link = book_feed.GetThumbnailLink().href.replace('zoom=5','zoom=1')

        book = models.Book()
        book.cache_book_info(google_id, save_cover=False)

        book_form = BookForm(
            {
             'title':book.title,
             'authors': ",".join(book._authors),
             'isbn10': book.isbn10,
             'isbn13': book.isbn13,
             'gid': book.gid,
             'description': book.description,
             'metarating': book.metarating,
             }
        )

        ctx.update({'book': book, 'book_form': book_form})

    return render_to_response(template_name, RequestContext(request, ctx))

def temp_(isbn):
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
def book_checkout(request, template_name="ebooks/checkout.html", *args, **kwargs):
    ctx = {}

    book_key = kwargs.get('book_key')
    ownership = get_object_or_404(models.Ownership, key__exact=book_key)
    users = User.objects.all()

    if request.POST:
        if request.POST.has_key('submit'):
            if request.POST['submit'] == "Checkout":
                checkout_form = forms.CheckOutForm(request.POST, users=users)
                if checkout_form.is_valid():
                    print "valid"
                    recipient_id = checkout_form.cleaned_data["to_who"]

                    checkout = models.CheckOut()
                    checkout.user = User.objects.get(id=recipient_id)
                    checkout.book = ownership
                    checkout.save()
                    ownership.checked_out = checkout
                    ownership.save()
            if request.POST['submit'] == "Checkin":
                checkout = ownership.checked_out
                checkout.check_in_time = datetime.now()
                checkout.save()

                ownership.checked_out = None
                ownership.save()

                checkout_form = forms.CheckOutForm(users=users)
                ctx['checkout_form'] = checkout_form
    else:
        checkout_form = forms.CheckOutForm(users=users)
        ctx['checkout_form'] = checkout_form

    ctx.update({'ownership': ownership})

    return render_to_response(template_name, RequestContext(request, ctx))


def view_tag(request, template_name="ebooks/view_tag.html", *args, **kwargs):
    ctx = {}

    tag = kwargs.get('tag')
    books = TaggedItem.objects.get_by_model(models.Book, tag)

    ctx.update({'tag':tag, 'books': books})
    return render_to_response(template_name, RequestContext(request, ctx))
