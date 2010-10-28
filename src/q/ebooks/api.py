import os.path
from tempfile import NamedTemporaryFile
import urllib2

from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from q.ebooks.models import Book, Format

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
