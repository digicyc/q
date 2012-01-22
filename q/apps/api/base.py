from tastypie.authentication import Authentication
from tastypie.resources import NamespacedModelResource, Resource
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
