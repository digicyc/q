import operator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import user_passes_test


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
