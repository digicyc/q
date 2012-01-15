from django.conf.urls.defaults import *
from tastypie.api import NamespacedApi
from api.resources.v2 import books

api = NamespacedApi(api_name='v2', urlconf_namespace='api')

# client
api.register(books.BookResource())


urlpatterns = patterns('',
    url(r'^', include(api.urls)),
)
