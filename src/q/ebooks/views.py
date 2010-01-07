from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from q.ebooks import models

def index(request):
    books = models.Book.objects.all()
    return render_to_response("ebooks/index.html",
        {
            'books': books,
        },
        context_instance=RequestContext(request)
    )


