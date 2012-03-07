from django.template import Library
register = Library()

@register.filter
def truncatechars(s, num):
    """
    Truncates a word after a given number of chars  
    Argument: Number of chars to truncate after
    """
    length = int(num)
    if len(s) > num:
        return s[0:num] + '...'
    return s