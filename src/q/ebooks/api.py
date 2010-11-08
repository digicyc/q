import os.path
from tempfile import NamedTemporaryFile
import urllib2

from django.utils import simplejson
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from tagging.models import Tag

from q.common import group_required
from q.ebooks.models import Book, Format, Ownership

@login_required
def email_kindle(request, book_id):
    """
    Email the mobi format of the book to the user's kindle email address
    """
    from django.core.mail import EmailMessage

    try:
        book = Book.objects.get(id=book_id)
    except:
        return HttpResponse('Fail')

    email = EmailMessage()
    email.subject = book.title
    email.body = book.description
    email.to = (request.user.get_profile().kindle_email,)
    email.bcc = ("",) # This is a hack. I don't know why you have to set this to "" but you do otherwise it gives errors

    headers = {'User-Agent': settings.DEFAULT_HTTP_HEADERS}
    url = Format.objects.filter(ebook=book, format='mobi')[0].ebook_file.url
    filename = os.path.basename(url)
    data = urllib2.urlopen(urllib2.Request(url, headers=headers)).read()

    email.attach(filename, data, 'application/x-mobipocket-ebook')
    email.send()

    return HttpResponse('Okay')

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