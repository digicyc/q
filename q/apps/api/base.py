from django.contrib.auth.models import User

from tastypie.authentication import Authentication
from tastypie.resources import NamespacedModelResource, Resource, Validation
from tastypie.authorization import Authorization as DjangoAuthorization

from ebooks import models
class DjangoAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if hasattr(request, 'user'):
            return request.user.is_authenticated()
        return False

    def get_identifier(self, request):
        return request.user.username

class NSResource(NamespacedModelResource):
    """
    Q Base Resource.

    Defines some common Meta options, like authorization, authentication,
    and urlconf_namespace
    """
    class Meta:
        urlconf_namespace = 'api'
        authorization = DjangoAuthorization()
        authentication = DjangoAuthentication()

class Resource(Resource):
    """
    Neutron Base Resource.

    Defines some common Meta options, like authorization, authentication,
    and urlconf_namespace
    """
    class Meta:
        urlconf_namespace = 'api'
        authorization = DjangoAuthorization()
        authentication = DjangoAuthentication()

class UserResource(Resource):
    class Meta(Resource.Meta):
        queryset = User.objects.all()
        resource_name = 'auth/user'
        allowed_methods = ['get']
        excludes = ['password', 'is_staff',]

class UserNSResource(NSResource):
    class Meta(NSResource.Meta):
        queryset = User.objects.all()
        resource_name = 'auth/user'
        allowed_methods = ['get']
        excludes = ['password', 'is_staff',]

class BookValidation(Validation):
    def is_valid(self, bundle, request=None):
        title = bundle.data.get('title', None)

        errors = dict()

        try:
            book = models.Book.objects.get(title=title)
            errors['title'] = "Duplicate title: %s. Has this book already been added?"\
                % (book.title,)
        except models.Book.DoesNotExist:
            pass

        return errors