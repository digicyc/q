import operator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import user_passes_test

from django.conf import settings

def admin_keyword_search(model, fields, keywords):
    """
    """
    if not keywords:
        return []

    keywords = keywords.split(" ")
    qs = QuerySet(model)
    for keyword in keywords:
        or_queries = [ Q(**{'%s__icontains' % field: keyword}) for field in fields ]
        other_qs = QuerySet(model)
        if qs.select_related:
            other_qs = other_qs.select_related()
        other_qs = other_qs.filter(reduce(operator.or_, or_queries))
        qs = qs & other_qs

    return qs

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            return u.get_profile().is_librarian
        return False
    return user_passes_test(in_groups)

def touch_wsgi(request):
    """
    This exists because beanstalkapp and pycharm both deploy files for me via SFTP. Each have web hooks of sites to call
    after the push is done and usually what needs to be done is the wsgi touched.
    """
    from django.http import HttpResponse
    if not request.GET.has_key('key'):
        return HttpResponse('False')
    if request.GET['key'] != "None" and request.GET['key'] == settings.WSGI_RELOAD_KEY:
        f = open(settings.WSGI_RELOAD_PATH,'w').close()
        return HttpResponse('True')
    return HttpResponse('False')
        