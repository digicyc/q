import os
from tempfile import NamedTemporaryFile
import urllib2

from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.db.models import ImageField

from django.conf import settings

from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from goodreads import GoodReads

from api import base
from ebooks import models

class AuthorResource(base.NSResource):
    class Meta(base.NSResource.Meta):
        queryset = models.Author.objects.all()
        resource_name = "books/author"
        filtering = {
            'id': ALL,
        }

class SeriesResource(base.NSResource):
    class Meta(base.NSResource.Meta):
        queryset = models.Series.objects.all()
        resource_name = "books/series"
        filtering = {
            'id': ALL,
        }
        ordering = ['-id',]

class BookResource(base.NSResource):
    authors = fields.ToManyField('api.resources.v2.books.AuthorResource', 'authors')

    class Meta(base.NSResource.Meta):
        queryset = models.Book.objects.all()
        resource_name = "books/book"
        validation = base.BookValidation()
        filtering = {
            'id': ALL,
        }
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

    def hydrate_cover(self, bundle):
        print "hydrating cover"
        #headers = {'User-Agent': settings.DEFAULT_HTTP_HEADERS}
        #f = NamedTemporaryFile(delete=False)
        #f.write(urllib2.urlopen(urllib2.Request(bundle.data["cover_url"], headers=headers)).read())
        #f.filename = f.name
        #f.close()
        #
        #print "----"
        #print f.name
        #bundle.obj.cover.save(
        #    "temp_filename.jpg",
        #    File(open(f.name))
        #)

        return bundle
        #os.unlink(f.name)

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

    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
            }

        return

    def obj_get(self, request=None, **kwargs):
        isbn = kwargs.get('isbn', None)
        return GoodReads(isbn)

    def get_object_list(self, request):
        results = []
        for isbn in request.REQUEST['isbn'].split(','):
            gr = self.obj_get(request, isbn=isbn)
            results.append(gr)
        return results

    def obj_get_list(self, request=None, **kwargs):
        # Filtering disabled for brevity...
        results = self.get_object_list(request)
        return results

    def full_dehydrate(self, bundle):
        bundle.data = bundle.obj.__dict__
        return bundle