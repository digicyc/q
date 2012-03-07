from ebooks.models import Format
from django.contrib.sites.models import Site

from django.conf import settings

def book_count_insert(request):
   count = Format.objects.all().values('ebook').distinct().count()
   return {'book_count': count}

def site_insert(request):
    site = Site.objects.get(pk=settings.SITE_ID)
    return {'site': site}

def version_insert(request):
    from q import __version__
    return {'version': __version__}

def hostname_insert(request):
    import socket
    hostname = socket.gethostname()
    if '.' in hostname:
        hostname = hostname.split('.')[0]
    return {'hostname': hostname}