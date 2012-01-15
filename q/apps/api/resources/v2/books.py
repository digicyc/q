from tastypie.resources import ALL

from api import base
from ebooks import models

class BookResource(base.NBResource):
    class Meta(base.NBResource.Meta):
        queryset = models.Book.objects.all()
        resource_name = "book"

        filtering = {
            'id': ALL,
        }