import os
from tempfile import NamedTemporaryFile
import urllib2

from django.core.files import File
from django.db.models.query import Q, QuerySet
from django.db import connection
from django.template.defaultfilters import slugify

from django.conf import settings

from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from goodreads import GoodReads
import googlebooks

from api import base
from ebooks import models


class AuthorResource(base.NSResource):
    class Meta(base.NSResource.Meta):
        queryset = models.Author.objects.all()
        resource_name = "books/author"
        filtering = {
            'id': ALL,
            'firstname': ALL_WITH_RELATIONS,
            'lastname': ALL_WITH_RELATIONS,
        }
        
    def get_object_list(self, request):
        """
        """    
        number = (len(request.GET)/2)
        if number < 2:
            return super(AuthorResource, self).get_object_list(request)
        cursor = connection.cursor()
        ids = list()
        for x in range(0, number):
            fn_val = request.GET["firstname%s__iexact" % x]
            ln_val = request.GET["lastname%s__iexact" % x]

            query = "SELECT id FROM ebooks_author WHERE firstname='%s' AND lastname='%s'" % (fn_val, ln_val)
            
            row = cursor.execute(query).fetchone()
            if row is not None:
                ids.append(row[0])
            else:
                author = models.Author()
                author.firstname = fn_val
                author.lastname = ln_val
                author.slug = slugify("%s %s" % (fn_val, ln_val))
                author.save()
                ids.append(author.id)
        authors = models.Author.objects.filter(id__in=ids)
        return authors

class SeriesResource(base.NSResource):
    class Meta(base.NSResource.Meta):
        queryset = models.Series.objects.all()
        resource_name = "books/series"
        filtering = {
            'id': ALL,
            'name': ALL_WITH_RELATIONS,
        }

class BookResource(base.NSResource):
    authors = fields.ToManyField('api.resources.v2.books.AuthorResource', 'authors')

    class Meta(base.NSResource.Meta):
        queryset = models.Book.objects.all()
        resource_name = "books/book"
        validation = base.BookValidation()
        filtering = {
            'id': ALL,
        }
        ordering = ["id",]
        allow_methods = ["get", "post", "put"]

    def save_m2m(self, bundle):
        super(BookResource, self).save_m2m(bundle)
        if bundle.data.has_key('cover_url'):
            headers = {'User-Agent': settings.DEFAULT_HTTP_HEADERS}
            f = NamedTemporaryFile(delete=False)
            f.write(urllib2.urlopen(urllib2.Request(bundle.data["cover_url"], headers=headers)).read())
            f.filename = f.name
            f.close()

            bundle.obj.cover.save("temp_name.jpg", File(open(f.name)))
            os.unlink(f.name)
        return bundle

class FormatResource(base.NSResource):
    book = fields.ForeignKey(BookResource, 'book')

    class Meta(base.NSResource.Meta):
        queryset = models.Format.objects.all()
        resource_name = "books/format"

        filtering = {
            'book': ALL_WITH_RELATIONS,
        }

    def hydrate(self, bundle):
        if "book_id" in bundle.data:
            bundle.obj.book = models.Book.objects.get(
                pk=bundle.data["book_id"])

class GoodReadsResource(base.Resource):
    class Meta(base.Resource.Meta):
        resource_name = "books/goodreads"
        object_class = GoodReads

    #def get_resource_uri(self, bundle_or_obj):
    #    kwargs = {
    #        'resource_name': self._meta.resource_name,
    #        }

    #   return

    def obj_get(self, request=None, **kwargs):

        isbn = kwargs.get('isbn', None)
        gr = GoodReads(isbn)
        g = googlebooks.GoogleBook(isbn)
        gr.authors = g.authors
        return gr

    def get_object_list(self, request):
        results = []
        for isbn in request.REQUEST['isbn'].split(','):
            gr = self.obj_get(request, isbn=isbn)
            results.append(gr)
        return results 

    def obj_get_list(self, request=None):
        # Filtering disabled for brevity...
        results = self.get_object_list(request)
        return results

    def full_dehydrate(self, bundle):
        bundle.data = bundle.obj.__dict__
        return bundle