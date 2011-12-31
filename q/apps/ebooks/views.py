import os.path
import re
import urllib2
from tempfile import NamedTemporaryFile
from base64 import b64decode
from datetime import datetime

from django.core.files import File
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.conf import settings

from tagging.models import TaggedItem, Tag

from activity_stream.models import create_activity_item
from activity_stream.models import ActivityStreamItem

from q.common import admin_keyword_search, superuser_only

from ebooks.admin import BookAdmin
from ebooks import models
from ebooks import forms
from accounts.models import UserDownload


@login_required
def index(request, template_name="ebooks/index.html"):
    """
    Defines the index of the site.
    """
    ctx = {}

    # Otherwise just display the 15 latest books.
    books = cache.get('index_latest_books')
    if books is None:
        books = models.Book.objects.order_by("-create_time")[:42].distinct()
        cache.set('index_latest_books', books, 60*60) #cache for 60min

    activity_stream = cache.get('index_activity_stream')
    if activity_stream is None:
        activity_stream = ActivityStreamItem.objects.filter(subjects__isnull=False).\
                            exclude(type__name='upload').\
                            exclude(type__name='download').\
                            exclude(type__name='kindle').\
                            order_by('-created_at').distinct()[:10]
        cache.set('index_activity_stream', activity_stream, 60*60)  #cache for 60min

    ctx['activity_stream'] = activity_stream

    #ctx['tags'] = Tag.objects.cloud_for_model(models.Book)
    ctx['books'] = books
    
    if request.session.has_key('show_welcome_message'):
        ctx['show_welcome_message'] = True
        del request.session['show_welcome_message']

    return render_to_response(template_name,
                              RequestContext(request, ctx))

@login_required
@superuser_only
def activity_stream(request, template_name='ebooks/activity_stream.html'):
    ctx = {}
    ctx['activity_stream'] = ActivityStreamItem.objects.filter(subjects__isnull=False).\
                    order_by('-created_at').distinct()[:10]
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
def books_by_type(request, template_name="ebooks/search.html", page_num=1, *args, **kwargs):
    """
    Browse books by the specified type.
    """
    ctx = {}

    num_per_page = 10
    filter_type = kwargs.get('type').lower()
    books = None

    if request.GET.has_key('q') and request.GET['q'].strip() != "":
        books = admin_keyword_search(models.Book,
            BookAdmin.search_fields, request.GET['q'])
    else:
        letter = kwargs.get('letter')
        ctx['letter'] = letter

        if filter_type == "author":
            if letter is not None:
                books = models.Book.objects.filter(authors__lastname__istartswith=letter).order_by('authors__lastname', 'authors__firstname')
            else:
                books = models.Book.objects.all().order_by('authors__lastname')
        elif filter_type == "title":
            if letter is not None:
                books = models.Book.objects.filter(Q(title__iregex=r'^(An|And|The) %s+' % letter) | Q(title__istartswith=letter)).\
                    extra(select={'order_title': 'REPLACE(LOWER(title), "the ", "")'}).\
                    order_by('order_title')
            else:
                books = models.Book.objects.all().order_by('title')

    paginator = Paginator(books, num_per_page)
    page = paginator.page(page_num)

    ctx['type'] = filter_type
    ctx['page'] = page
    return render_to_response(template_name,
                              RequestContext(request, ctx))

@login_required
def books_by_series(request, template_name="ebooks/search.html",  *args, **kwargs):
    """
    Display the books for a given series.
    """
    ctx = {}

    slug = kwargs.get('series_slug').lower()

    series = models.Series.objects.filter(slug__exact=slug)
    books = models.Book.objects.filter(series=series).order_by('series_num')

    ctx['books'] = books
    return render_to_response(template_name,
                              RequestContext(request, ctx))

def latest_books_rss(request, template_name="ebooks/latest_books.rss"):
    """
    Return an RSS feed with the latest 10 books uploaded
    """
    ctx = {}
    books = models.Book.objects.all().order_by("-create_time")[:10]

    ctx.update({ 'books': books })
    return render_to_response(template_name,
                              RequestContext(request, ctx))

@login_required
def book_info(request, template_name="ebooks/book_info.html", *args, **kwargs):
    """
    Display the information for the book
    """
    ctx = {}

    book_slug = kwargs.get('book_slug')

    book = get_object_or_404(models.Book, slug=book_slug)

    error = None
    if request.FILES.has_key("book"):
        # We are getting a book uploaded
        filename = request.FILES["book"].name
        ext = os.path.splitext(filename)[1].replace('.','')
        if (ext, ext) not in models.FORMAT_CHOICES:
            error = "invalid filetype: %s" % filename

        if not error:
            try:
                format = models.Format.objects.get(ebook=book, format=ext)
                error = "Format exists: %s" % format.format

            except models.Format.DoesNotExist:
                format = models.Format()
                format.ebook = book
                format.format = ext
                format.uploaded_by = request.user

                f = NamedTemporaryFile(delete=False)
                f.write(request.FILES["book"].read())
                f.filename = filename
                f.close()

                format.ebook_file.save(
                    "temp_filename.%s" % ext,
                    File(open(f.name))
                )

                format.save()
                os.unlink(f.name)

                #activity stream
                create_activity_item('upload', request.user, format)


    # see if the logged in user has read this book to display the check
    try:
        read = models.Read.objects.get(user=request.user, book=book)
    except models.Read.DoesNotExist:
        read = None
    checkouts = models.CheckOut.objects.filter(book__book=book).order_by('-create_time')
    format_form = forms.UploadFormatForm()

    try:
        my_ownership = models.Ownership.objects.get(book=book, user=request.user)
    except models.Ownership.DoesNotExist:
        my_ownership = None

    ctx.update(
        {
            'book': book,
            'checkouts':checkouts,
            'my_ownership': my_ownership,
            'format_form': format_form,
            'error': error,
            'read': read,
        }
    )

    return render_to_response(template_name,
                              RequestContext(request, ctx))

@login_required
def add_book(request, isbn=None, template_name="ebooks/add/index.html", *args, **kwargs):
    """
    Begins the add book wizard process
    """
    from ebooks.forms import BookForm
    ctx = {}

    book_form = BookForm()
    book = models.Book()

    if request.POST.has_key('title'):
        try:
            book = models.Book.objects.get(isbn13=request.POST['isbn13'])
        except models.Book.DoesNotExist:
            book = None
        
        if book is not None:
            messages.error(request, "You are trying to add a duplicate book.")
            
            ctx.update({'book_form': BookForm(request.POST)})
            return render_to_response(template_name,
                              RequestContext(request, ctx))
        
        book = models.Book()
        book.title = request.POST['title']
        book.isbn10 = request.POST['isbn10']
        book.isbn13 = request.POST['isbn13']
        book.gid = request.POST['gid']
        book.description = request.POST['description']
        book.tags = ''

        #book.save()
        #book.tags = request.POST['tags']
        book.save()
        for gauthor in request.POST['authors'].split(','):
            try:
                author = models.Author.objects.get(firstname=" ".join(gauthor.split(" ")[:-1]).strip(), lastname=gauthor.split(" ")[-1])
            except models.Author.DoesNotExist:
                author = models.Author()
                author.firstname = " ".join(gauthor.split(" ")[:-1]).strip()
                author.lastname = gauthor.split(" ")[-1]
                author.save()
            book.authors.add(author)

        if book.cover == "" and request.POST.has_key('cover_url') and request.POST['cover_url'] != "":
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

        if request.POST["series"] != "":
            series_name = request.POST["series"]
            series_num = request.POST["series_num"]
            try:
                series = models.Series.objects.get(name__exact=series_name)
            except models.Series.DoesNotExist:
                series = models.Series()
                series.name = series_name
                series.save()
            book.series = series
            book.series_num = series_num
        book.save()

        return HttpResponseRedirect(reverse(book_info, kwargs={'book_slug': book.slug}))

    if request.POST.has_key("isbn") and isbn is None:
        isbn = re.sub("\D", "", request.POST['isbn'])

    if isbn:
        from gdata.books import BookFeed
        from urllib2 import urlopen

        search_xml = urlopen("http://books.google.com/books/feeds/volumes?q=ISBN%s" % isbn).read()
        search_feed = BookFeed.FromString(search_xml)
        google_id = search_feed.entry[0].identifier[0].text

        #volume_xml = urlopen("http://www.google.com/books/feeds/volumes/%s" % google_id).read()
        #book_feed = Book.FromString(volume_xml)

        #cover_link = book_feed.GetThumbnailLink().href.replace('zoom=5','zoom=1')

        book.cache_book_info(google_id, save_cover=False)

        book_form = BookForm(
            {
             'title':book.title,
             'authors': ",".join(book._authors),
             'isbn10': book.isbn10,
             'isbn13': book.isbn13,
             'gid': book.gid,
             'description': book.description,
             'metarating': 0.0 if book.metarating is None else book.metarating,
             }
        )
        # Dupe check
        try:
            book = models.Book.objects.get(isbn13=book.isbn13)
            messages.error(request, "You are trying to add a duplicate book.")
        except models.Book.DoesNotExist:
            pass
            
    ctx.update({'book': book, 'book_form': book_form})
    return render_to_response(template_name,
                              RequestContext(request, ctx))

@login_required
def book_checkout(request, template_name="ebooks/checkout.html", *args, **kwargs):
    ctx = {}

    book_key = kwargs.get('book_key')
    ownership = get_object_or_404(models.Ownership, key__exact=book_key)
    users = User.objects.all()
    checkout_form = forms.CheckOutForm(users=users)

    if request.POST:
        if request.POST.has_key('submit'):
            if request.POST['submit'] == "Checkout":
                checkout_form = forms.CheckOutForm(request.POST, users=users)
                if checkout_form.is_valid():
                    recipient_id = checkout_form.cleaned_data["to_who"]

                    checkout = models.CheckOut()
                    checkout.user = User.objects.get(id=recipient_id)
                    checkout.book = ownership
                    if request.POST.has_key('notes'):
                        checkout.notes = request.POST['notes']
                    checkout.save()
                    ownership.checked_out = checkout
                    ownership.save()

                    #activity stream
                    create_activity_item('checkout', checkout.user, ownership)

            if request.POST['submit'] == "Checkin":
                checkout = ownership.checked_out
                checkout.check_in_time = datetime.now()
                checkout.save()

                ownership.checked_out = None
                ownership.save()

                #activity stream
                create_activity_item('checkin', checkout.user, ownership)

                checkout_form = forms.CheckOutForm(users=users)

    ctx.update({'ownership': ownership, 'checkout_form': checkout_form})

    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
def view_tag(request, template_name="ebooks/view_tag.html", *args, **kwargs):
    ctx = {}

    tag = kwargs.get('tag')
    books = TaggedItem.objects.get_by_model(models.Book, [tag,])

    ctx.update({'tag':tag, 'books': books})
    return render_to_response(template_name, RequestContext(request, ctx))

@login_required
def download_format(request, *args, **kwargs):
    download_key = kwargs.get('download_key')

    book_info = b64decode(download_key).split('::')

    download_url = book_info[0]
    book = models.Book.objects.get(pk__exact=book_info[1])
    book_format = book_info[2]

    # count the download towards the user.
    user_download = UserDownload()
    user_download.user = request.user
    user_download.book =book
    user_download.format = book_format
    user_download.save()

    #activity stream
    create_activity_item('download', request.user, user_download)

    return HttpResponseRedirect(download_url)

@login_required
def books_missing_tags(request):
    books = models.Book.objects.all()
    untagged_books=[]
    for book in books:
        if len(book.tags) < 4:
            untagged_books.append(book)
    
    return render_to_response('ebooks/contribute/by_tags.html', RequestContext(request, {'books': untagged_books}))

@login_required
def books_missing_covers(request):
    books = models.Book.objects.filter(cover='')
    
    return render_to_response('ebooks/contribute/by_tags.html', RequestContext(request, {'books': books}))
