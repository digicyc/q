from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from goodreads import GoodReads

from api import base
from ebooks import models


class BookResource(base.NSResource):
    class Meta(base.NSResource.Meta):
        queryset = models.Book.objects.all()
        resource_name = "books/book"

        filtering = {
            'id': ALL,
        }

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

        return uri

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