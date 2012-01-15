from tastypie.authentication import Authentication
from tastypie.resources import NamespacedModelResource
from django.contrib.auth.models import User

## TODO; change this when you're done testing
from tastypie.authorization import Authorization as DjangoAuthorization

class DjangoAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if hasattr(request, 'user'):
            return request.user.is_authenticated()
        return False

    def get_identifier(self, request):
        return request.user.username

class NBResource(NamespacedModelResource):
    """
    Neutron Base Resource.

    Defines some common Meta options, like authorization, authentication,
    and urlconf_namespace
    """
    class Meta:
        urlconf_namespace = 'api'
        authorization = DjangoAuthorization()
        authentication = DjangoAuthentication()

class UserResource(NBResource):
    class Meta(NBResource.Meta):
        queryset = User.objects.all()
        resource_name = 'auth/user'
        allowed_methods = ['get']
        excludes = ['password', 'is_staff',]
