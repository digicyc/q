from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie import fields

from actstream import models as actstream_models

from api import base

class ActivityStreamResource(base.NSResource):
    class Meta(base.NSResource.Meta):
        queryset = actstream_models.Action.objects.all()
        resource_name = "accounts/activity_stream"