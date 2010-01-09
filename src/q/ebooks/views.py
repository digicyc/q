from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from q.common import admin_keyword_search

from q.ebooks.admin import BookAdmin
from q.ebooks import models

def index(request):
    """
    Search for a book
    """

    if request.GET.has_key('q') and request.GET['q'].strip() != "":
        books = admin_keyword_search(models.Book,
                BookAdmin.search_fields, request.GET['q'])
    else:
        books = models.Book.objects.all().order_by('author__lastname')

    return render_to_response("ebooks/index.html",
        {
            'books': books,
        },
        context_instance=RequestContext(request)
    )

