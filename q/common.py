from math import sqrt
import os
import operator

from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.utils.functional import lazy
from django.core.urlresolvers import reverse


from django.conf import settings

reverse_lazy = lazy(reverse, str)


def superuser_only(function):
    """
    Limit view to superusers only.
    """
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner

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

@csrf_exempt
def touch_wsgi(request):
    """
    This exists because beanstalkapp and pycharm both deploy files for me via SFTP. Each have web hooks of sites to call
    after the push is done and usually what needs to be done is the wsgi touched.
    """
    from django.http import HttpResponse, Http404
    from django.utils import simplejson

    if not request.GET.has_key('key'):
        raise Http404()
    if request.GET['key'] != "None" and request.GET['key'] == settings.WSGI_RELOAD_KEY:
        f = open(settings.WSGI_RELOAD_PATH,'a')
        os.utime(settings.WSGI_RELOAD_PATH, None)
        f.close()

        return HttpResponse('True')
    raise Http404

def similarity(algo="pearson", *args, **kwargs):
    return algo(*args, **kwargs)

def pearson(prefs_dict, obj1, obj2):
    """
    compare preferences between obj1 and obj2
    """
    related_items = dict()

    for item in prefs_dict[obj1]:
        if item in prefs_dict[obj2]:
            related_items[item] = True

    n = len(related_items)

    if not n: return 0

    # Add all prefs
    sum1 = sum(prefs_dict[obj1][item] for item in prefs_dict)
    sum2 = sum(prefs_dict[obj2][item] for item in prefs_dict)

    # Sum up the squares
    sum1_sq = sum([pow(prefs_dict[obj1][item],2) for item in prefs_dict])
    sum2_sq = sum([pow(prefs_dict[obj2][item],2) for item in prefs_dict])

    # Sum up the products
    p_sum = sum([prefs[obj1][item]*prefs[obj2][item] for item in prefs_dict])

    # Calculate Pearson score
    numerator = p_sum-(sum1*sum2/n)
    denominator = sqrt((sum1_sq-pow(sum1,2)/n)*(sum2_sq-pow(sum2,2)/n))
    if not denominator: return 0

    return numerator/denominator