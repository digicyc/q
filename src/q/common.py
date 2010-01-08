import operator
from django.db.models import Q
from django.db.models.query import QuerySet

def admin_keyword_search(model, fields, keywords):
    """
    """

    if not keywords:
        return []

    qs = QuerySet(model)
    for keyword in keywords:
        or_queries = [ Q(**{'%s__icontains' % field: keyword}) for field in fields ]
        other_qs = QuerySet(model)
        if qs.select_related:
            other_qs = other_qs.select_related()
        other_qs = other_qs.filter(reduce(operator.or_, or_queries))
        qs = qs & other_qs

    return qs
