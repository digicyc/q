from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from q.common import admin_keyword_search

from q.ebooks.admin import BookAdmin
from q.ebooks import models

#@login_required
def index(request):
    """
    Search for a book
    """
    books = None
    if request.GET.has_key('q') and request.GET['q'].strip() != "":
        books = admin_keyword_search(models.Book,
                BookAdmin.search_fields, request.GET['q'])

    return render_to_response("ebooks/index.html",
        {
            'books': books,
        },
        context_instance=RequestContext(request)
    )

def books_by_type(request, type, letter="a"):
    """
    Browse books by author
    """
    if type.lower() == "author":
        books = models.Book.objects.filter(author__lastname__istartswith=letter)
    elif type.lower() == "title":
        books  = models.Book.objects.filter(title__istartswith=letter)

    return render_to_response("ebooks/index.html",
        {
            'books': books,
        },
        context_instance=RequestContext(request)
    )

