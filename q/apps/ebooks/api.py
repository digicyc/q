import os.path
import urllib2

from django.utils import simplejson
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

from tagging.models import Tag
from activity_stream.models import create_activity_item

from q.common import group_required
from ebooks.models import Book, Format, Ownership

@login_required
def email_kindle(request, book_id):
    """
    Email the mobi format of the book to the user's kindle email address
    """
    from django.core.mail import EmailMessage

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book id: %s not found" % book_id)
        return HttpResponseRedirect(reverse('ebooks.views.index'))

    email = EmailMessage()
    email.subject = book.title
    email.body = book.description
    email.to = [request.user.get_profile().kindle_email,]

    headers = {'User-Agent': settings.DEFAULT_HTTP_HEADERS}
    url = Format.objects.filter(ebook=book, format='mobi')[0].ebook_file.url
    filename = os.path.basename(url)
    data = urllib2.urlopen(urllib2.Request(url, headers=headers)).read()

    email.attach(filename, data, 'application/x-mobipocket-ebook')
    email.send()

    create_activity_item('kindle', request.user, book)

    messages.success(request, "Successfully sent %s!" % book.title)
    return HttpResponseRedirect(reverse('ebooks.views.book_info', kwargs={'book_slug': book.slug}))

@login_required
@group_required('Librarian')
def change_book_attribute(request, book_id):
    """
    Changes the book's attribute
    """
    if not request.POST:
        return HttpResponse('Fail')

    attribute = None
    if request.POST.has_key('name'):
        attribute = request.POST['name']
    else:
        return HttpResponse('Fail')

    if request.POST.has_key("info"):
        book = Book.objects.get(id=book_id)
        if hasattr(book, attribute):
            setattr(book, attribute, request.POST["info"])
            book.save()

            return HttpResponse('Okay')

    return HttpResponse('Fail')

@login_required
def get_tags(request):

    q = request.GET.get('q')
    tags = Tag.objects.filter(name__startswith=q)
    taglist = [tag.name for tag in tags]

    return HttpResponse("\n".join(taglist), mimetype='text/plain')
    
@login_required
def update_tag(request):
    tags = request.POST.getlist('tags[]')
    tag_list = ",".join(tags)

    book_id = request.POST.get('book_id')
    book = Book.objects.get(id=book_id)
    
    Tag.objects.update_tags(book, tag_list)

    return HttpResponse('Success')

@login_required
def i_own_this_book(request):
    
    response_dict = {}
    response_dict['success'] = True

    book_id = request.GET.get('book_id')
    book = Book.objects.get(pk=book_id)
    
    try:
        ownership = Ownership.objects.get(book=book, user=request.user)
        response_dict['remove_ownership'] = {'id':ownership.pk}
        
        ownership.delete()
    except Ownership.DoesNotExist:
        ownership = Ownership()
        ownership.user = request.user
        ownership.book = book
        ownership.save()
        response_dict['ownership'] = {'key': ownership.key, 'qr_code':ownership.qr_url}
    
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

@login_required
def toggle_verify(request):
    response_dict = dict()
    response_dict['error'] = False
    
    if request.method == "POST":
        format = None

        if request.POST.has_key('format_id'):
            from ebooks.models import Format
            try:
                format = Format.objects.get(pk=request.POST['format_id'])
            except Format.DoesNotExist:
                response_dict['error'] = True
                response_dict['msg'] = "Cannot find format for book."

        else:
            resonse_dict['error'] = True
            response_dict['msg'] = "Missing format_id paramter"
            
        if request.POST.has_key('is_verified'):
            verified = request.POST['is_verified']
            if verified.lower() == "true":
                verified = True
            else:
                verified = False
        else:
            verified = not format.verified

        if not response_dict['error']:
            format.verified = bool(verified)
            format.save()
            response_dict['msg'] = "Success!"

    else:
        response_dict['error'] = True
        response_dict['msg'] = "Expecting POST data"

    return HttpResponse(simplejson.dumps(response_dict),
                        mimetype='applicaiton/json')